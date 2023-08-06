#!/usr/bin/env python
#
# This file is part of SharedArray.
# Copyright (C) 2014-2017 Mathieu Mirmont <mat@parad0x.org>
#
# SharedArray is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# SharedArray is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SharedArray.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup, Extension
from glob import glob
from os import path
import sys
import numpy

# Convert a file to reStructuredText with pypandoc, when available,
# otherwise return the raw file.
def convert_to_rst(filename):
    try:
        import pypandoc
        return pypandoc.convert(filename, 'rst')

    except ImportError:
        return open(filename).read()

setup(name    = 'SharedArray',
      version = '2.0.3',

      # Description
      description      = 'Share numpy arrays between processes',
      long_description = convert_to_rst('README.md'),

      # Contact
      author       = 'Mathieu Mirmont',
      author_email = 'mat@parad0x.org',
      url          = 'https://gitlab.com/tenzing/shared-array',

      # License
      license   = 'https://www.gnu.org/licenses/gpl-2.0.html',

      # Extras for pip
      keywords  = 'numpy array shared memory shm',
      classifiers  = [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: C',
          'Topic :: Scientific/Engineering'
      ],

      # Compilation
      ext_modules  = [
          Extension('SharedArray',
                    glob(path.join('.', 'src', '*.c')),
                    libraries = [ 'rt' ] if sys.platform.startswith('linux') else [],
                    include_dirs=[numpy.get_include()])
      ])
