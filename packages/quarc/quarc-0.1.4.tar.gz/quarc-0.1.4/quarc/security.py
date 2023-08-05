# Copyright (C) 2017 Simon Biggs
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# http://www.gnu.org/licenses/.
"""Create x509 certificates for use https access."""

import os
from getpass import getpass
import datetime
import ipaddress

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

from ipython_genutils.path import ensure_dir_exists
from jupyter_core.paths import jupyter_data_dir


QUARC_DATA_DIRECTORY = os.path.join(
    os.path.split(jupyter_data_dir())[0], 'quarc')
AUTH_FILEPATH = os.path.join(QUARC_DATA_DIRECTORY, "auth_token.txt")

CERT_DIRECTORY = os.path.join(QUARC_DATA_DIRECTORY, "certificates")
CERT_AUTHORITY_DIRECTORY = os.path.join(CERT_DIRECTORY, "authority")

SALT_FILEPATH = os.path.join(CERT_DIRECTORY, "salt")
PASSPHRASE_FILEPATH = os.path.join(CERT_DIRECTORY, "passphrase")

CERT_FILENAME = "cert.crt"
KEY_FILENAME = "key.pem"


def create_certificate(ip):
    certificate_filepath = os.path.join(CERT_DIRECTORY, ip, CERT_FILENAME)
    key_filepath = os.path.join(CERT_DIRECTORY, ip, KEY_FILENAME)

    ca_certificate_filepath = os.path.join(
        CERT_AUTHORITY_DIRECTORY, CERT_FILENAME)
    ca_key_filepath = os.path.join(
        CERT_AUTHORITY_DIRECTORY, KEY_FILENAME)

    ensure_dir_exists(CERT_DIRECTORY, mode=0o700)
    ensure_dir_exists(CERT_AUTHORITY_DIRECTORY, mode=0o700)
    
    if os.path.exists(PASSPHRASE_FILEPATH):
        prompt = 'Passphrase: '
    else:
        prompt = 'Define passphrase: '

    passphrase = getpass(prompt=prompt).encode()

    if os.path.exists(PASSPHRASE_FILEPATH):
        with open(SALT_FILEPATH, 'rb') as file:
            salt = file.read()

        with open(PASSPHRASE_FILEPATH, 'rb') as file:
            passphrase_key = file.read()

        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        
        kdf.verify(passphrase, passphrase_key)

    else:
        salt = os.urandom(16)
        with open(SALT_FILEPATH, 'wb') as file:
            file.write(salt)

        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )

        passphrase_key = kdf.derive(passphrase)

        with open(PASSPHRASE_FILEPATH, 'wb') as file:
            file.write(passphrase_key)

    quarc_ca = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "AU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "NSW"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Wagga Wagga"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Quarc"),
        x509.NameAttribute(NameOID.COMMON_NAME, "quarc.services")
    ])

    if not os.path.exists(ca_key_filepath):
        ca_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(ca_key_filepath, 'wb') as file:
            file.write(
                ca_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.BestAvailableEncryption(passphrase)
                )
            )

        subject = issuer = quarc_ca

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            ca_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=3650)
        ).sign(ca_key, hashes.SHA256(), default_backend())

        with open(ca_certificate_filepath, 'wb') as file:
            file.write(cert.public_bytes(serialization.Encoding.PEM))

        # print(
        #     "\n"
        #     "================================================================="
        #     "==============="
        #     "\n\n"
        #     "  A unique root certificate has been created at:\n\n"
        #     "      {}\n\n"
        #     "  This certificate needs to be installed as a certificate authority\n"
        #     "  on each client that needs to access this server.\n\n"
        #     "  WARNING: By installing this certificate you are aware that\n"
        #     "  browsers will trust any website which can sign with the private\n"
        #     "  key which has just been created at the following location:\n\n"
        #     "      {}\n\n"
        #     "  This private key is encrypted with the passphrase you just\n"
        #     "  provided. This private key is unique to your installation. Do not\n"
        #     "  share your encryption passphrase or the private key.\n\n"
        #     "================================================================="
        #     "==============="
        #     "\n".format(ca_certificate_filepath, ca_key_filepath))



    if os.path.exists(certificate_filepath) & os.path.exists(key_filepath):
        pass

    else:
        ensure_dir_exists(os.path.join(CERT_DIRECTORY, ip), mode=0o700)

        with open(ca_key_filepath, 'rb') as file:
            ca_key = serialization.load_pem_private_key(
                file.read(), 
                password=passphrase,
                backend=default_backend())

        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(key_filepath, 'wb') as file:
            file.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.BestAvailableEncryption(
                        passphrase)
                )
            )

        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "AU"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "NSW"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Wagga Wagga"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Quarc Kernel"),
            x509.NameAttribute(NameOID.COMMON_NAME, ip)
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            quarc_ca
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=3652)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.IPAddress(ipaddress.ip_address(ip))]),
            critical=True,
        ).sign(ca_key, hashes.SHA256(), default_backend())

        with open(certificate_filepath, 'wb') as file:
            file.write(cert.public_bytes(serialization.Encoding.PEM))


        print(
            "\n"
            "================================================================="
            "==============="
            "\n\n"
            "  An ssl certificate for your current IP address has been created at:\n\n"
            "      {}\n\n"
            "  This certificate is to be installed on each client that needs\n"
            "  access to this server. This will inform browsers to trust this\n"
            "  server while it is hosted at:\n\n"
            "      https://{}:PORT\n\n"
            "  So that this process does not need to be repeated this server\n"
            "  should have a static IP.\n\n"
            "================================================================="
            "==============="
            "\n".format(certificate_filepath, ip))


    return passphrase, certificate_filepath, key_filepath