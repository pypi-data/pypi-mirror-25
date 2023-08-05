# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import sys

try:
    import __pypy__
except ImportError:
    __pypy__ = None

__version__ = None
here = os.path.abspath(os.path.dirname(__file__))
name = 'watchm8'

with open('%s/requirements.txt' % here) as f:
    requires = f.readlines()

with open('%s/version.txt' % here) as f:
    __version__ = f.readline().strip()

with open('%s/README.md' % here) as f:
    readme = f.readline().strip()

macros = []

if __pypy__ is not None:
    macros.append(('_PYPY', '1'))
elif sys.version_info.major == 2:
    macros.append(('_PYTHON2', '1'))
elif sys.version_info.major == 3:
    macros.append(('_PYTHON3', '1'))

setup(
    name=name,
    version=__version__,
    description=(
        'Event driven "If This Then That" like automation tool for '
        'watchable resources'
    ),
    long_description=readme,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    author='Simon Pirschel',
    author_email='simon@aboutsimon.com',
    url='https://github.com/freach/watchm8',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    scripts=['scripts/m8.py'],
)
