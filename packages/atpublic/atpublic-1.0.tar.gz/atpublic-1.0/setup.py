# Copyright (C) 2016-2017 Barry Warsaw
#
# This project is licensed under the terms of the Apache 2.0 License.  See
# LICENSE.txt for details.

import os

from setup_helpers import get_version, require_python
from setuptools import setup, find_packages, Extension

require_python(0x30400f0)
__version__ = get_version('public/__init__.py')


# It can be a pain in some environments to build the C extension module.  For
# example, if you're using tox on a platform that doesn't have a C compiler.
# OTOH, we can be more efficient with the C extension.  In order to give
# environments the option to build what they want, we'll only build the C
# extension if this environment variable is set.

ext_modules = []
if os.getenv('ATPUBLIC_BUILD_EXTENSION', False):
    ext_modules.append(Extension('_public', ['src/public.c']))


setup(
    name='atpublic',
    version=__version__,
    description='public -- @public for populating __all__',
    long_description="""\
This is a very simple decorator and function which populates a module's
__all__ and optionally the module globals.

This provides both a pure-Python implementation and a C implementation.  It is
proposed that the C implementation be added to builtins_ for Python 3.6.
""",
    author='Barry Warsaw',
    author_email='barry@python.org',
    license='Apache 2.0',
    url='http://public.readthedocs.io/',
    packages=find_packages(),
    include_package_data=True,
    ext_modules=ext_modules,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        ]
    )
