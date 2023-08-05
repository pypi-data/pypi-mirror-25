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
import base64
import datetime
import ipaddress

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

from ipython_genutils.path import ensure_dir_exists
from jupyter_core.paths import jupyter_data_dir


QUARC_DATA_DIRECTORY = os.path.join(
    os.path.split(jupyter_data_dir())[0], 'quarc')
AUTH_FILEPATH = os.path.join(QUARC_DATA_DIRECTORY, "auth_token.txt")

CERT_DIRECTORY = QUARC_DATA_DIRECTORY

CERT_FILENAME = "cert.crt"
KEY_FILENAME = "key.pem"

SERVER_DIRNAME = "server"
AUTHORITY_DIRNAME = "authority"

DEFAULT_ENTROPY = 32


def get_filepaths(ip, dirname):
    directory = os.path.join(
        CERT_DIRECTORY, ip, dirname)

    ensure_dir_exists(directory, mode=0o700)

    cert_filepath = os.path.join(directory, CERT_FILENAME)
    key_filepath = os.path.join(directory, KEY_FILENAME)

    return cert_filepath, key_filepath


def make_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )


def get_persistent_key(key_filepath):
    if not os.path.exists(key_filepath):
        key = make_key()

        with open(key_filepath, 'wb') as file:
            file.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
    else:
        with open(key_filepath, 'rb') as file:
            key = serialization.load_pem_private_key(
                file.read(), 
                password=None,
                backend=default_backend())

    return key


def authority_certificate(ip):
    auth_cert_filepath, _ = get_filepaths(
        ip, AUTHORITY_DIRNAME)

    auth_key = make_key()

    issuer = subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "AU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "NSW"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Wagga Wagga"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Quarc"),
        x509.NameAttribute(NameOID.COMMON_NAME, "quarc.services")
    ])

    if os.path.exists(auth_cert_filepath):
        # print(
        #     "\nTLS authority certificate:\n"
        #     "    {}\n".format(auth_cert_filepath))
        pass
    else:
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
            "  A TLS certificate for your current IP address has been created at:\n\n"
            "      {}\n\n"
            "  This certificate is to be installed as a certificate authority\n"
            "  on each client that needs access to this server. This certificate\n"
            "  will only allow authentication for servers hosted at the followng\n"
            "  address:\n\n"
            "      https://{}:PORT\n\n"
            "  This is achieved by implementing the Name Constraints extension\n"
            "  and by not storing the certificate authority private key to disk.\n\n"
            "================================================================="
            "==============="
            "\n".format(auth_cert_filepath, ip))

    return auth_cert_filepath, subject, auth_key


def server_certificate(ip, issuer, issuer_key):
    server_cert_filepath, server_key_filepath = get_filepaths(
        ip, SERVER_DIRNAME)
    
    server_key = get_persistent_key(server_key_filepath)
    
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
        ).sign(issuer_key, hashes.SHA256(), default_backend())


        with open(server_cert_filepath, 'wb') as file:
            file.write(cert.public_bytes(serialization.Encoding.PEM))


    return server_cert_filepath, server_key_filepath


def create_certificate(ip):
    ensure_dir_exists(CERT_DIRECTORY, mode=0o700)

    auth_cert_filepath, issuer, issuer_key = authority_certificate(ip)
    cert_filepath, key_filepath = server_certificate(ip, issuer, issuer_key)

    return auth_cert_filepath, cert_filepath, key_filepath


def make_token(n):
    return base64.urlsafe_b64encode(os.urandom(n)).rstrip(b'=').decode('ascii')


def get_auth_token():
    if os.path.exists(AUTH_FILEPATH):
        with open(AUTH_FILEPATH, 'r') as file:
            auth_token = file.read()
    else:
        auth_token = make_token(DEFAULT_ENTROPY)
        with open(AUTH_FILEPATH, 'w') as file:
            file.write(auth_token)

    return auth_token