# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.2'


setup(
    name='pywe-ticket',
    version=version,
    keywords='Wechat Weixin Ticket',
    description='Wechat Ticket Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/sdkwe/pywe-ticket',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pywe_ticket'],
    py_modules=[],
    install_requires=['pywe_base', 'pywe_exception', 'pywe_storage', 'pywe_token>=1.0.7'],

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
