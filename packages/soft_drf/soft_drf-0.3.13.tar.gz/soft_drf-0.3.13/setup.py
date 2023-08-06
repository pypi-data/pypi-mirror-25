#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from soft_drf import __author__, __version__

setup(
    name='soft_drf',
    version=__version__,
    description=(
        'Mixins and templates to do scaffolding with '
        'Django Rest Framework project.'
    ),
    author=__author__,
    author_email='angel.david.lagunas@gmail.com',
    url='https://github.com/angellagunas/soft_drf',
    download_url=(
        'https://github.com/angellagunas/soft_drf/archive/{0}.tar.gz'.format(
            __version__
        )
    ),
    install_requires=[
        'Django==1.11.4',
        'django-cors-headers==2.1.0',
        'djangorestframework==3.6.4',
        'djangorestframework-camel-case==0.2.0',
        'djangorestframework-jwt==1.11.0',
        'drf-nested-routers==0.90.0'
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
