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

import os
import socket
import webbrowser
import signal
from multiprocessing import Process

import tornado.ioloop
import tornado.web

from notebook.notebookapp import NotebookApp
# DEV = True

from .security import create_certificate, get_auth_token
from ._version import __version__

KERNEL_PORT = 17575
CERTIFICATE_PORT = 19393


class FileHandler(tornado.web.StaticFileHandler):
    def initialize(self, path):
        self.dirname, self.filename = os.path.split(path)
        super(FileHandler, self).initialize(self.dirname)

    def get(self, path=None, include_body=True):
        self.set_header(
            'Content-Disposition', 'attachment; filename={}'.format(
                self.filename))
        super(FileHandler, self).get(self.filename, include_body)


def stop_tornado():
    tornado.ioloop.IOLoop.instance().stop()


def serve_certificate(filepath):
    app = tornado.web.Application([
        (r'/', FileHandler, {'path': filepath})
    ])

    app.listen(CERTIFICATE_PORT)

    signal.signal(signal.SIGTERM, stop_tornado)
    
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass


class Quarc(NotebookApp):
    name = 'quarc'
    version = __version__
    description = """
        Quarc

        Provides kernel access to https://quarc.services.
    """


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except:
        ip = socket.gethostbyname(socket.gethostname())

    auth_cert_filepath, certificate, key = create_certificate(ip)
    
    allow_origin='https://quarc.services'
    # if DEV:
    #     allow_origin='http://localhost:4200'

    auth_token = get_auth_token()

    print(
        '\nConnect to this server by going to the following URL in your browser:')
    
    url = '{}?ip={}&token={}\n'.format(
        allow_origin, ip, auth_token)
    print('    {}'.format(url))
    webbrowser.open(url)

    print('Authority certificate hosted at http://{}:{}'.format(
        ip, CERTIFICATE_PORT))

    Process(
        target=serve_certificate,
        args=(auth_cert_filepath,)).start()

    Quarc.launch_instance(
        port=KERNEL_PORT, ip=ip, port_retries=0,
        allow_origin=allow_origin,
        certfile=certificate, 
        keyfile=key,
        token=auth_token,
        open_browser=False,
        tornado_settings={
            "xsrf_cookies": False
        })


if __name__ == "__main__":
    main()