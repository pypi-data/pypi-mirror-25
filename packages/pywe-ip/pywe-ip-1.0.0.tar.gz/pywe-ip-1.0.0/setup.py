# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.0'


setup(
    name='pywe-ip',
    version=version,
    keywords='Wechat Weixin Media',
    description='Wechat IP Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/sdkwe/pywe-ip',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pywe_ip'],
    py_modules=[],
    install_requires=['pywe_base>=1.0.3', 'pywe_token>=1.0.6'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
