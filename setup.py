#!/usr/bin/env python

from distutils.core import setup

setup(name='openstore-cli',
      version='0.7',
      description='CLI tool for the OpenStore app store service. Manage or search apps for your Ubuntu Touch device.',
      author='Marius Gripsgard',
      author_email='me@mariogrip.com',
      url='https://code.launchpad.net/~mariogrip/openstore-tool/trunk',
      packages=['openstorecli'],
      scripts=['openstore-cli'],
      install_requires=[
          'requests'
      ]
     )
