#!/usr/bin/env python3
from setuptools import setup  ,find_packages
install_modules=['bs4','requests','tushare','lxml']
setup(name='yxspkg',   
      version='2.8.8',    
      description='My pypi module',    
      author='Blackso',    
      install_requires=install_modules,
      author_email='1185793964@qq.com',       
      url='http://weibo.com/2320090895/profile',
      packages=find_packages(), 
      classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
)   