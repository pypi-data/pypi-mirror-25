#!/usr/bin/env python

from setuptools import setup, Extension

long_description = """
=======
SEGY IO
=======

Introduction
------------

Segyio is a small LGPL licensed C library for easy interaction with SEG Y
formatted seismic data, with language bindings for Python and Matlab. Segyio is
an attempt to create an easy-to-use, embeddable, community-oriented library for
seismic applications. Features are added as they are needed; suggestions and
contributions of all kinds are very welcome.

Feature summary
---------------
 * A low-level C interface with few assumptions; easy to bind to other
   languages.
 * Read and write binary and textual headers.
 * Read and write traces, trace headers.
 * Easy to use and native-feeling python interface with numpy integration.

Project goals
-------------

Segyio does necessarily attempt to be the end-all of SEG-Y interactions;
rather, we aim to lower the barrier to interacting with SEG-Y files for
embedding, new applications or free-standing programs.

Additionally, the aim is not to support the full standard or all exotic (but
correctly) formatted files out there. Some assumptions are made, such as:

 * All traces in a file are assumed to be of the same sample size.
 * It is assumed all lines have the same number of traces.

The writing functionality in Segyio is largely meant to *modify* or adapt
files. A file created from scratch is not necessarily a to-spec SEG-Y file, as
we only necessarily write the header fields segyio needs to make sense of the
geometry. It is still highly recommended that SEG-Y files are maintained and
written according to specification, but segyio does not mandate this.

"""

setup(name='segyio',
      version='1.3.3',
      description='Simple & fast IO for SEG-Y files',
      long_description=long_description,
      author='Statoil ASA',
      author_email='fg_gpl@statoil.com',
      url='https://github.com/Statoil/segyio',
      packages=['segyio'],
      package_data={'': ['License', 'README']},
      license='LGPL-3.0',
      ext_modules=[Extension('segyio._segyio',
                                                sources=['pycmake/src/python/segyio/_segyio.c','pycmake/src/lib/src/segy.c'],
                                                include_dirs=['pycmake/include/lib/src','pycmake/include/lib/include'],
                                                define_macros=[('HAVE_NETINET_IN_H', None),('HAVE_MMAP', None),('HAVE_SYS_STAT_H', None)],
                                                library_dirs=[],
                                                libraries=['m'],
                                                extra_compile_args=['-std=c99'])],
      platforms='any',
      requires=['numpy'],
      install_requires=['numpy'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities'
      ]
      )
