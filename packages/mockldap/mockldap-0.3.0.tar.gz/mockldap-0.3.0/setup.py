#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import setup


def readall(path):
    with open(path) as fp:
        return fp.read()


setup(
    name='mockldap',
    version='0.3.0',
    description="A simple mock implementation of python-ldap.",
    long_description=readall('README'),
    url='http://bitbucket.org/psagers/mockldap/',
    author='Peter Sagerson',
    author_email='psagers@ignorare.net',
    license='BSD',
    packages=['mockldap'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
    ],
    keywords=['mock', 'ldap'],
    install_requires=[
        'funcparserlib == 0.3.6',

        'pyldap; python_version >= "3.0"',
        'python-ldap >= 2.0; python_version < "3.0"',

        'mock; python_version < "3.0"',
    ],
    setup_requires=[
        'setuptools >= 0.6c11',
    ],
    test_suite='tests',
)
