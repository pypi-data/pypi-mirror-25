# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from fredlibs.version import __version__
version = __version__

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='fredlibs',
    version=version,
    description='fredlibs package',
    long_description=readme,
    author='Fred Vassard',
    author_email='azafred@gmail.com',
    url='https://github.com/azafred/fredlibs',
    download_url='https://github.com/azafred/fredlibs/archive/0.1.tar.gz',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=required,
    tests_require=['nose', 'testfixtures', 'mock'],
    test_suite="nose.collector",
    py_modules=['fredlibs'],
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

