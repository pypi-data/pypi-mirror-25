#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import crm_groups

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = crm_groups.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='ar-crm-groups',
    version=version,
    description="""Your project description goes here""",
    long_description=readme + '\n\n' + history,
    author='arteria GmbH',
    author_email='admin@arteria.ch',
    url='https://github.com/arteria/ar-crm-groups',
    packages=[
        'crm_groups',
    ],
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    license="BSD",
    zip_safe=False,
    keywords='ar-crm-groups',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
