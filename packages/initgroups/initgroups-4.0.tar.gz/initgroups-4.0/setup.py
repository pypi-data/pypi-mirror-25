##############################################################################
#
# Copyright (c) 2010 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from setuptools import setup
from setuptools import find_packages

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

setup(name='initgroups',
      version='4.0',
      url='https://github.com/zopefoundation/initgroups',
      license='ZPL 2.1',
      description="Convenience uid/gid helper function used in Zope2.",
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      long_description=README + '\n' + CHANGES,
      keywords=["deprecated", "uid", "gid", "Zope2"],
      classifiers=[
          "Development Status :: 7 - Inactive",
          "Framework :: Zope2",
          "License :: OSI Approved :: Zope Public License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=True)
