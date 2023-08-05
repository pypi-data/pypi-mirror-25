#!/usr/bin/env python
"""
 Copyright (C) 2016 by SolarWinds, LLC.
 All rights reserved.
"""

import distutils.ccompiler
import os
import sys
from setuptools import setup, Extension

version = '2.0.0b1'


def python_version_supported():
    if sys.version_info[0] == 2:
        if sys.version_info[1] not in (6, 7):
            return False
    elif sys.version_info[0] == 3:
        if sys.version_info[1] < 3:
            return False
    return True


def os_supported():
    return sys.platform.startswith('linux')


if not python_version_supported():
    sys.exit('This package supports only Python 2.6, 2.7, 3.3 and above on Linux.')

# conditionally build extensions if liboboe is available on this platform
# otherwise, will function in no-op mode: no tracing, but all API endpoints available
compiler = distutils.ccompiler.new_compiler()
if compiler.has_function('oboe_metadata_init', libraries=('oboe-1.0',), library_dirs=('appoptics/swig',)):
    appoptics_module = Extension('appoptics.swig._oboe',
                                 sources=['appoptics/swig/oboe_wrap.cxx'],
                                 depends=['appoptics/swig/oboe.hpp'],
                                 include_dirs=['appoptics/swig', 'appoptics'],
                                 libraries=['oboe-1.0'],
                                 library_dirs=['appoptics/swig'],
                                 runtime_library_dirs=['$ORIGIN'])
    ext_modules = [appoptics_module]
else:
    ext_modules = []

# compiler.has_function doesn't clean up after itself https://bugs.python.org/issue25544
if os.path.exists('a.out'):
    os.remove('a.out')

setup(name='appoptics',
      version=version,
      author='SolarWinds, LLC',
      author_email='support@appoptics.com',
      url='https://www.appoptics.com/apm/python',
      download_url='https://pypi.python.org/pypi/appoptics',
      description='AppOptics libraries, instrumentation, and web middleware components '
                  'for WSGI, Django, and Tornado.',
      long_description=open('README.md').read(),
      keywords='appoptics traceview tracelytics oboe liboboe instrumentation performance wsgi middleware django',
      ext_modules=ext_modules,
      packages=['appoptics', 'appoptics.swig'],
      package_data={'appoptics': ['swig/liboboe-1.0.so.0']},
      license='LICENSE.txt',
      install_requires=['decorator', 'six'],
      )
