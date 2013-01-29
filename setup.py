#!/usr/bin/env python
"""
sentry-quotas
=============

An extension for Sentry which allows setting hard quotas.

:copyright: (c) 2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


tests_require = [
    'exam',
    'mock',
    'pytest',
    'pytest-django',
    'unittest2',
]

install_requires = [
    'nydus',
    'redis',
    'sentry>=5.0.0',
]

setup(
    name='sentry-quotas',
    version='0.1.5',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/getsentry/sentry-quotas',
    description='A Sentry extension which add hard limits to projects.',
    long_description=__doc__,
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'quotas = sentry_quotas',
        ],
       'sentry.plugins': [
            'quotas = sentry_quotas.plugin:QuotasPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
