#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'raven>=6.1.0',
    'fluent-logger>=0.5.3',
    'six>=1.10.0'
]

setup_requirements = [
]

test_requirements = [
]

description = "A transport for raven-python which supports fluentd."

setup(
    name='raven_fluentd',
    version='0.1.2',
    description=description,
    long_description=description,
    author="Yuichiro Someya",
    author_email='me@ayemos.me',
    url='https://github.com/ayemos/raven-transports-fluentd-python',
    packages=find_packages(include=['raven_fluentd', 'raven_fluentd.transport']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='raven fluentd',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
