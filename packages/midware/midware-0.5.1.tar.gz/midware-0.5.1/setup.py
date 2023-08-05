# -*- coding: utf-8 -*-

from setuptools import setup

import midware

midware_classifiers = [
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

with open('README.md') as f:
    midware_long_description = f.read()

with open('LICENSE') as f:
    midware_license = f.read()

setup(
    name='midware',
    version=midware.__version__,
    description='A simple general-purpose middleware library for Python',
    long_description=midware_long_description,
    author='Ivan Dmitrievsky',
    author_email='ivan.dmitrievsky+python@gmail.com',
    url='https://github.com/idmit/midware',
    tests_require=["pytest"],
    py_modules=["midware"],
    license=midware_license,
    classifiers=midware_classifiers, )
