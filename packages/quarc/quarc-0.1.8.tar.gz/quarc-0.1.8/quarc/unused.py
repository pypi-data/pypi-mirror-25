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
"""Useful function that was pulled out of use."""

import os
import ssl

from getpass import getpass

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from traitlets import Unicode, default
from jupyter_core.paths import jupyter_data_dir
from kernel_gateway.gatewayapp import KernelGatewayApp

from ._version import __version__

QUARC_DATA_DIRECTORY = os.path.join(
    os.path.split(jupyter_data_dir())[0], 'quarc')

CERT_DIRECTORY = QUARC_DATA_DIRECTORY

SALT_FILEPATH = os.path.join(CERT_DIRECTORY, "salt")
PASSPHRASE_FILEPATH = os.path.join(CERT_DIRECTORY, "passphrase")


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