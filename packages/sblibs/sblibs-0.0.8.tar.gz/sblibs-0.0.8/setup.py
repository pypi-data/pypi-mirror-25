# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from sblibs.version import __version__
version = __version__

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sblibs',
    version=version,
    description='sblibs package',
    long_description=readme,
    author='Fred Vassard',
    author_email='fred@studyblue.com',
    url='https://github.com/studyblue/sblibs',
    download_url='https://github.com/studyblue/sblibs/archive/{}.tar.gz'.format(version),
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=required,
    tests_require=['nose', 'testfixtures', 'mock'],
    test_suite="nose.collector",
    py_modules=['sblibs'],
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License'
    ]
)