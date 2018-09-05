#!/usr/bin/env python

from distutils.core import setup

setup(
    name='openstore-cli',
    version='0.8',
    description='CLI tool for the OpenStore app store service. Manage or search apps for your Ubuntu Touch device.',
    author='Marius Gripsgard',
    author_email='me@mariogrip.com',
    url='https://github.com/UbuntuOpenStore/openstore-uploader-tool',
    packages=['openstorecli'],
    scripts=['openstore-cli'],
    install_requires=[
        'requests'
    ]
)
