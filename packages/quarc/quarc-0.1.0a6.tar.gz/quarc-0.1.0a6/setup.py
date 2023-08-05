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
import sys
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(here, 'quarc', '_version.py')) as file:
    exec(file.read(), {}, version_ns)

setup(
    name = "quarc",
    version = version_ns['__version__'],
    author = "Simon Biggs",
    author_email = "mail@simonbiggs.net",
    description = "Open a Quarc Gateway",
    long_description = """This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.""",
    keywords = [],
    packages = [
        "quarc"
    ],
    entry_points={
        'console_scripts': [
            'quarc=quarc:main',
        ],
    },
    license='AGPL3+',
    install_requires=[
        'jupyter_kernel_gateway',
        'cryptography'
    ],
    classifiers = [],
    url = "https://quarc.services/"
)