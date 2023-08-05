# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:32:21 2016

@author: 
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""


from setuptools import setup

setup(
    name = 'mytools',      # The name of the PyPI-package.
    packages = ['mytools'],
    version = '1.1.2',    # Update the version number for new releases
    #scripts=['ngtsio'],  # The name of the included script(s), and also the command used for calling it
    description = 'Set of tools for photometric time series data and plotting',
    author = 'Maximilian N. Guenther',
    author_email = 'mg719@cam.ac.uk',
    url = 'https://github.com/MNGuenther/mytools',
    download_url = 'https://github.com/MNGuenther/mytools/releases',
    classifiers = [],
    install_requires=['numpy>=1.10','matplotlib>0.1','scipy>=0.1','pandas>=0.1']
    )



