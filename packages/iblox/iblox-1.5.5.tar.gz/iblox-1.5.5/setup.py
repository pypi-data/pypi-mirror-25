#!/usr/bin/env python
# coding=utf-8
"""Setup file for iblox module
"""

from setuptools import setup

setup(name='iblox',
      version='1.5.5',
      description='Infoblox WAPI Module',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      url='http://iblox.readthedocs.io/',
      py_modules=['iblox'],
      license='GNU Lesser General Public License v3 or later (LGPLv3+)',
      install_requires=['requests>=2.11.0'],
      tests_require=['simplejson','future'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Development Status :: 5 - Production/Stable',
          'Operating System :: Unix',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
