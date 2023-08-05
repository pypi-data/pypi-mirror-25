#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="deploybot-client",
    test_suite='test',
    version='0.0.1',
    description=u"Deploybot API Client",
    long_description=u"Deploybot API Client",
    classifiers=[],
    keywords='deploy,service,api,client,sdk,deploybot,continuous,delivery,cd',
    author=u"Thiago Paes",
    author_email='mrprompt@gmail.com',
    url='https://github.com/mrprompt/deploybot-client',
    license='GPL',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    extras_require={
        'test': ['pytest', 'pytest-cov', 'mock', 'unittest-data-provider'],
    }
)
