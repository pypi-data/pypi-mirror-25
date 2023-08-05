#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: seefeel
# date: 2017-08-24

from setuptools import setup

setup(name='seefeel',
      username='seefeel',
      version='0.1.1',
      description='utils for text preprocess',
      url='https://github.com/LeslieFire/seefeel',
      author='seefeel',
      author_email='249893977@qq.com',
      license='MIT',
      packages=['seefeel'],
      package_dir={'seefeel': 'seefeel'},
      package_data={'seefeel':['*.*', 'seefeel/*']},
      zip_safe=False)
