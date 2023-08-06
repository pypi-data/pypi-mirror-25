#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'cinder',
    'pyotp==2.2.6',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='cinder_auths',
    version='0.1.1',
    description="Cinder Authentication Examples",
    long_description=readme + '\n\n' + history,
    author="Gorka Eguileor",
    author_email='gorka@eguileor.com',
    url='https://github.com/akrog/cinder_auths',
    packages=[
        'cinder_auths',
    ],
    package_dir={'cinder_auths':
                 'cinder_auths'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='cinder_auths',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'paste.filter_factory': [
            'otp=cinder_auths:otp_factory',
            'plain_pwd=cinder_auths:plain_pwd_factory',
        ]
    }
)
