#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

py_major_minor = '{0[0]}.{0[1]}'.format(sys.version_info)


def read(fn):
    with open(os.path.join(os.path.dirname(__file__), fn)) as f:
        return f.read()


# Read version from source file
version = {}
exec(read('src/hesong/utils/version.py'), version)
__version__ = version['__version__']

# Dependencies by version
install_requires = []
if py_major_minor < '3.4':
    install_requires.append('enum34')

# setup configurations
setup(
    name='hesong-utils',
    version=__version__,
    namespace_packages=['hesong'],
    packages=find_packages('src', exclude=['tests', 'docs']),
    package_dir={'': 'src'},  # tell distutils packages are under src
    url='http://bitbucket.org/hesong-opensource/hesong-python-utils',
    license='BSD',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    description='Hesong Python Utils',
    long_description=read('README.rst'),
    # Requires-Python version.
    python_requires='>=2.6',
    # Dependencies Declarations
    install_requires=install_requires,
    extras_require={
        'product': ['ujson', 'PyYAML'],
    }
)
