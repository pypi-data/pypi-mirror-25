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

import socket
import os
import sys
import ssl
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



from traitlets import Unicode, default

from kernel_gateway.gatewayapp import KernelGatewayApp

from ._version import __version__

CERT_DIRECTORY = "certificates"
CERT_AUTHORITY_DIRECTORY = os.path.join(CERT_DIRECTORY, "authority")
CERT_FILENAME = "certificate.crt"
KEY_FILENAME = "key.pem"
AUTH_FILE = "auth_token.txt"
SALT_FILEPATH = os.path.join(CERT_DIRECTORY, "salt")
PASSPHRASE_FILEPATH = os.path.join(CERT_DIRECTORY, "passphrase")


class Quarc(KernelGatewayApp):
    name = 'quarc'
    version = __version__
    description = """
        Quarc

        Provides kernel access to https://quarc.services.
    """

    # SSL Passphrase
    passphrase_env = 'QU_PASSPHRASE'
    passphrase = Unicode(config=True,
        help='Passphrase for SSL certificates (QU_PASSPHRASE env var)'
    )

    @default('passphrase')
    def _passphrase_default(self):
        return os.getenv(self.passphrase_env, '')


    def _build_ssl_options(self):       
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(
            self.certfile, self.keyfile, password=self.passphrase)

        return ssl_ctx


def create_certificate(ip):
    certificate_filepath = os.path.join(CERT_DIRECTORY, ip, CERT_FILENAME)
    key_filepath = os.path.join(CERT_DIRECTORY, ip, KEY_FILENAME)

    ca_certificate_filepath = os.path.join(
        CERT_AUTHORITY_DIRECTORY, CERT_FILENAME)
    ca_key_filepath = os.path.join(
        CERT_AUTHORITY_DIRECTORY, KEY_FILENAME)

    if not os.path.exists(CERT_DIRECTORY):
        os.mkdir(CERT_DIRECTORY)

    if not os.path.exists(CERT_AUTHORITY_DIRECTORY):
        os.mkdir(CERT_AUTHORITY_DIRECTORY)

    if not os.path.exists(PASSPHRASE_FILEPATH):
        print(
            "Create a passphrase to encrypt your server certificate key. You "
            "will be prompted for this passphrase each time the server starts."
            " This passphrase will only need to be used on the server."
        )
        
    passphrase = getpass(prompt='Passphrase: ').encode()

    if os.path.exists(PASSPHRASE_FILEPATH):
        passphrase_match = False
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
        # store passphrase
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

        print(
            "A unique root certificate has been created at {}. On each "
            "computer that needs to access this server you need to install "
            "this certificate. Follow steps outlined for your browser and os "
            "that are provided when googling `installing root certificate`.\n"
            "WARNING: By installing this certificate you are aware that "
            "browsers will trust any website which can sign with the private "
            "key located at {}. This private key is encrypted with the "
            "passphrase you just provided. This private key is unique to your "
            "installation. Do not share your encryption passphrase.".format(
                ca_certificate_filepath, ca_key_filepath))


    if os.path.exists(certificate_filepath) & os.path.exists(key_filepath):
        pass

    else:        
        if not os.path.exists(os.path.join(CERT_DIRECTORY, ip)):
            os.mkdir(os.path.join(CERT_DIRECTORY, ip))

        with open(ca_key_filepath, 'rb') as file:
            ca_key = serialization.load_pem_private_key(
                file.read(), 
                password=passphrase,
                backend=default_backend())

        # create a key pair
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
                    encryption_algorithm=serialization.BestAvailableEncryption(passphrase)
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


    return passphrase, certificate_filepath, key_filepath


def main():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, 'r') as file:
            auth_token = file.read()
    else:
        auth_token = input('Define client api token: ')
        with open(AUTH_FILE, 'w') as file:
            file.write(auth_token)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except:
        ip = socket.gethostbyname(socket.gethostname())

    passphrase, certificate, key = create_certificate(ip)
    
    allow_origin='https://quarc.services'

    if len(sys.argv) > 0:
        if sys.argv[-1] == 'dev':
            allow_origin='http://localhost:4200'

    print("Allowing access from: {}".format(allow_origin))
    print("Authentication token: {}".format(auth_token))

    Quarc.launch_instance(
        port=7575, ip=ip, port_retries=0,
        allow_credentials='true',
        auth_token=auth_token,
        allow_origin=allow_origin,
        allow_headers='X-XSRFToken,Content-Type,Authorization',
        allow_methods="DELETE,POST,OPTIONS",
        certfile=certificate, 
        keyfile=key,
        passphrase=passphrase)


if __name__ == "__main__":
    main()