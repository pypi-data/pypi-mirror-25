# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup


def get_requirements():
    with open('requirements/production.txt') as f:
        requirements = f.readlines()
    return requirements


def get_long_description():
    with open('README.md') as f:
        long_description = f.read()
    return long_description


setup(
    name='Flask-RESTive-MongoDB',
    version='0.0.1',
    url='https://github.com/left-join/flask-restive-mongodb',
    download_url='https://github.com/left-join/flask-restive-mongodb.git',
    license='MIT',
    author='left-join',
    author_email='left-join@riseup.net',
    description='Flask-RESTive extension to work with MongoDB.',
    long_description=get_long_description(),
    packages=['flask_restive_mongodb'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_requirements(),
    keywords=['Flask-RESTive', 'MongoDB'],
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
