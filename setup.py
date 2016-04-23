#!/usr/bin/env python

from distutils.core import setup

setup(name='open-uApp',
      version='0.7',
      description='A tool for manage the repo of the OpenStore app for Ubuntu touch',
      author='Marius Gripsgard',
      author_email='me@mariogrip.com',
      url='https://code.launchpad.net/~mariogrip/openstore-tool/trunk',
      packages=['openUapp'],
      scripts=['open-uapp'],
      install_requires=[
          'requests'
      ]
     )
