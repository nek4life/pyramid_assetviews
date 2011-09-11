import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'webob',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='pyramid_assetviews',
      version='1.0a2',
      description='pyramid_assetviews',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Charlie Choiniere',
      author_email='pylons-discuss@googlegroups.com',
      url='https://github.com/nek4life/pyramid_assetviews',
      keywords='pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyramid_assetviews',
      install_requires = requires,
      )

