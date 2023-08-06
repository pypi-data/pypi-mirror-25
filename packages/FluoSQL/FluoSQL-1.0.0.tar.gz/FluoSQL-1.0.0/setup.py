#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages

import FluoSQL
setup(
    name = 'FluoSQL',
    version = FluoSQL.__version__,
    author = 'Cyril Coelho',
    author_email = 'informabox.contact@gmail.com',
    maintainer = 'Cyril Coelho',
    maintainer_email = 'informabox.contact@gmail.com',
 
 
    packages=find_packages(),
 

 
    description="Connecteur SQL via HTTP & Outils SQL",
 
    long_description=open('README.md').read(),
 
    include_package_data=False,
 
    url='https://gitlab.com/LaGvidilo/FluoSQL',
  
    #download_url = 'https://gitlab.com/LaGvidilo/FluoSQL'

    classifiers=[
        "Programming Language :: Python",
        "Topic :: Communications",
    ],
 
    license="COPYLEFT"


)