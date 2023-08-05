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

from traitlets import Unicode, default
from kernel_gateway.gatewayapp import KernelGatewayApp

from .security import create_certificate, AUTH_FILEPATH, QUARC_DATA_DIRECTORY
from ._version import __version__


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


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except:
        ip = socket.gethostbyname(socket.gethostname())

    passphrase, certificate, key = create_certificate(ip)
    
    allow_origin='https://quarc.services'
    if sys.argv[-1] == 'dev':
        allow_origin='http://localhost:4200'

    print("Allowing kernel access from: {}".format(allow_origin))

    if os.path.exists(AUTH_FILEPATH):
        with open(AUTH_FILEPATH, 'r') as file:
            auth_token = file.read()
    else:
        auth_token = input('Define client API token: ')
        with open(AUTH_FILEPATH, 'w') as file:
            file.write(auth_token)

    print("Client API token: {}".format(auth_token))

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