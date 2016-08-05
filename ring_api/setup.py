#
# Copyright (C) 2016 Savoir-faire Linux Inc
#
# Author: Seva Ivanov <seva.ivanov@savoirfairelinux.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.
#

import sys, distutils
from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext

except ImportError:
    sys.exit('You need to install Cython=0.24')

if (not distutils.spawn.find_executable('dring')):
    sys.exit('You need to install Ring-daemon')

setup(
    name='ring_api',
    version='0.1.0.dev1',
    description='Exposing Ring-daemon using Cython',
    url='https://github.com/sevaivanov/ring-api',
    author='Seva Ivanov',
    author_email='seva.ivanov@savoirfairelinux.com',
    license='GPLv3+',
    keywords='ring ring.cx ring-api ring_api',
    #packages=find_packages(exclude=[''])
    install_requires=[
        'Cython',
        'flask',
        'flask_restful',
        'websockets'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # TODO test earlier
        'Programming Language :: Python :: 3.5',
    ],

    # Generate shared library
    ext_modules = cythonize(
        Extension(
            'ring_api',
            sources=[
                'wrappers/ring_api.pyx',
                'callbacks/cb_client.cpp'
            ],
            language='c++',
            extra_compile_args=[
                '-std=c++11'
            ],
            extra_link_args=[
                '-std=c++11'
            ],
            include_dirs = [
                '/usr/include/dring',
                'extra/hpp/',
                'callbacks/',
                'wrappers/'
            ],
            libraries=[
                'ring'
            ],
        )
    ),
    cmdclass = {
        'build_ext' : build_ext
    }
)
