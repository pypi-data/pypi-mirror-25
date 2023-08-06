""" Copyright (c) Trainline Limited, 2016. All rights reserved. See LICENSE.txt in the project root for license information. """
from setuptools import setup

setup(name='pyclingmerv',
      version='0.2.15',
      install_requires=['requests', 'simplejson'],
      license='Apache 2.0',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5'],
      package_data={'': ['LICENSE.txt']},
      packages=['environment_manager'],
      zip_safe=True)
