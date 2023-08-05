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
    name='Flask-Settings',
    version='0.0.3',
    url='https://github.com/left-join/flask-settings',
    download_url='https://github.com/left-join/flask-settings.git',
    license='MIT',
    author='left-join',
    author_email='left-join@riseup.net',
    description='Flask settings extension is similar to Django settings.',
    long_description=get_long_description(),
    packages=['flask_settings'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_requirements(),
    keywords=['flask', 'settings'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
    ]
)
