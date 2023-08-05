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

# CERT_DIRECTORY = os.path.join(QUARC_DATA_DIRECTORY, "certificates")
CERT_DIRECTORY = QUARC_DATA_DIRECTORY
SALT_FILEPATH = os.path.join(CERT_DIRECTORY, "salt")
PASSPHRASE_FILEPATH = os.path.join(CERT_DIRECTORY, "passphrase")

CERT_FILENAME = "cert.crt"
KEY_FILENAME = "key.pem"

SERVER_DIRNAME = "server"
AUTHORITY_DIRNAME = "authority"


def get_passphrase():
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

    return passphrase


def get_filepaths(ip, dirname):
    directory = os.path.join(
        CERT_DIRECTORY, ip, dirname)

    ensure_dir_exists(directory, mode=0o700)

    cert_filepath = os.path.join(directory, CERT_FILENAME)
    key_filepath = os.path.join(directory, KEY_FILENAME)

    return cert_filepath, key_filepath


def get_key(ip, key_filepath, passphrase):

    if not os.path.exists(key_filepath):
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
    else:
        with open(key_filepath, 'rb') as file:
            key = serialization.load_pem_private_key(
                file.read(), 
                password=passphrase,
                backend=default_backend())


    return key


def authority_certificate(ip, passphrase):
    auth_cert_filepath, auth_key_filepath = get_filepaths(
        ip, AUTHORITY_DIRNAME)
    
    auth_key = get_key(ip, auth_key_filepath, passphrase)

    issuer = subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "AU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "NSW"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Wagga Wagga"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Quarc"),
        x509.NameAttribute(NameOID.COMMON_NAME, "quarc.services")
    ])

    if not os.path.exists(auth_cert_filepath):
        # Uses name constraints
        # https://nameconstraints.bettertls.com/

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            auth_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=3650)
        ).add_extension(
            x509.NameConstraints([
                x509.IPAddress(ipaddress.ip_network(ip))], None),
            critical=True,
        ).sign(auth_key, hashes.SHA256(), default_backend())


        with open(auth_cert_filepath, 'wb') as file:
            file.write(cert.public_bytes(serialization.Encoding.PEM))

        print(
            "\n"
            "================================================================="
            "==============="
            "\n\n"
            "  An ssl certificate for your current IP address has been created at:\n\n"
            "      {}\n\n"
            "  This certificate is to be installed as a certificate authority\n"
            "  on each client that needs access to this server. This\n"
            "  has a constrained signing space by implemententing the Name\n"
            "  Constraints extension. This certificate should only be able to\n"
            "  get browsers to trust the server while it is hosted at:\n\n"
            "      https://{}:PORT\n\n"
            "  So that the certificate installtion process does not need to be\n"
            "  repeated this server should have a static IP.\n\n"
            "  To verify that your OS and browser respect Name Constraints\n"
            "  vist https://nameconstraints.bettertls.com/\n\n"
            "================================================================="
            "==============="
            "\n".format(auth_cert_filepath, ip))

    return subject


def server_certificate(ip, passphrase, issuer):
    _, auth_key_filepath = get_filepaths(ip, AUTHORITY_DIRNAME)
    server_cert_filepath, server_key_filepath = get_filepaths(
        ip, SERVER_DIRNAME)
    
    auth_key = get_key(ip, auth_key_filepath, passphrase)
    server_key = get_key(ip, server_key_filepath, passphrase)\
    
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "AU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "NSW"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Wagga Wagga"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Quarc"),
        x509.NameAttribute(NameOID.COMMON_NAME, "quarc.internal")
    ])

    if not os.path.exists(server_cert_filepath):
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            server_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=3650)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.IPAddress(ipaddress.ip_address(ip))]),
            critical=True,
        ).sign(auth_key, hashes.SHA256(), default_backend())


        with open(server_cert_filepath, 'wb') as file:
            file.write(cert.public_bytes(serialization.Encoding.PEM))


    return server_cert_filepath, server_key_filepath


def create_certificate(ip):
    ensure_dir_exists(CERT_DIRECTORY, mode=0o700)
    passphrase = get_passphrase()

    issuer = authority_certificate(ip, passphrase)
    cert_filepath, key_filepath = server_certificate(ip, passphrase, issuer)

    return passphrase, cert_filepath, key_filepath