# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path
setup(
    name='multilabel-metrics',
    version='0.0.1',
    description='Multilabel classification metrics for Python',
    long_description=open('README.txt').read(),
    url='https://github.com/hell-sing/multi-label-metrics',
    author=u'Abhishek Verma',
    author_email='abhishek_verma@hotmail.com',
    license='GNU_GPL licence, see LICENCE.txt',
	classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='classification metrics machine-learning ',
    py_modules=["mlmetrics"],
)
