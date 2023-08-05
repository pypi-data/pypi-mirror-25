# coding:utf-8

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 6):
    error = 'ERROR: gyun-sdk requires Python Version 2.6 or above.'
    print >> sys.stderr, error
    sys.exit(1)


setup(
    name='gyun-sdk',
    version='1.1.2',
    description='Software Development Kit for GYUN.',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    keywords='gyun iaas gomestor sdk',
    author='GYUN Team',
    author_email='service@gomeholdings.com',
    url='https://docs.qc.gyun.com/sdk/',
    packages=['gyun', 'gyun.conn', 'gyun.iaas',
              'gyun.misc', 'gyun.gomestor'],
    package_dir={'gyun-sdk': 'gyun'},
    namespace_packages=['gyun'],
    include_package_data=True,
    install_requires=['future']
)
