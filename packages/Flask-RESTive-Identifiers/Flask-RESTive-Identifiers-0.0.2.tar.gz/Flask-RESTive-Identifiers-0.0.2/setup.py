# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import platform
from setuptools import setup


def get_requirements():
    with open('requirements/production.txt') as f:
        requirements = f.readlines()

    platform_name = platform.python_implementation().lower()
    with open('requirements/platform_{0}.txt'.format(platform_name)) as f:
        requirements.extend(f.readlines())

    return requirements


def get_long_description():
    with open('README.md') as f:
        long_description = f.read()
    return long_description


setup(
    name='Flask-RESTive-Identifiers',
    version='0.0.2',
    url='https://github.com/left-join/flask-restive-identifiers',
    download_url='https://github.com/left-join/flask-restive-identifiers.git',
    license='MIT',
    author='left-join',
    author_email='left-join@riseup.net',
    description='Flask-RESTive extension to work with identifiers.',
    long_description=get_long_description(),
    packages=['flask_restive_identifiers'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_requirements(),
    keywords=['Flask-RESTive', 'generate', 'id'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
