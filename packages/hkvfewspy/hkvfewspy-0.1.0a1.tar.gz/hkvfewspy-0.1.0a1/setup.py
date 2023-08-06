#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages
setup(name='hkvfewspy',
      version='0.1.0a1',
      description='HKV tools voor operationeel waterbeheer',
      url='https://github.com/HKV-products-services/hkvfewspy',
      author='Mattijn van Hoek',
      author_email='mattijn.vanhoek@hkv.nl',
      license='BSD 3-Clause "New" or "Revised" license',
      keywords='hkv fews pi fews-pi fewspy',      
      packages=find_packages(),
      install_requires=[
          'zeep',
          'pytz',
          'numpy',
          'pandas'
      ],
      dependency_links=[
        'http://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona',
        'http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal',
        'http://geopandas.org/install.html'
        ],
      python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',        
     )