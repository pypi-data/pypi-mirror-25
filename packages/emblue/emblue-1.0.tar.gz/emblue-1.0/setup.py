#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setuptools import setup

setup(name='emblue',
      version='1.0',
      description='Utilizar el api de emblue',
      url='https://github.com/erickhein/emblue',
      author='Erick Hein',
      author_email='erickhv@gmail.com',
      license='None',
      classifiers=['Development Status :: 3 - Alpha','Intended Audience :: Developers','Topic :: Software Development :: Build Tools','Programming Language :: Python :: 2.7'],
      packages=['emblue'],
      install_requires=['requests'],
      zip_safe=False)

