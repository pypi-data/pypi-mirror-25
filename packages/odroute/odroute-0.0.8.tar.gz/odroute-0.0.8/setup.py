# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

INSTALL_REQUIREMENTS = [
    'Click>=6.0,<7.0',
    'pyzmq>=16.0,<17.0',
    'tornado>=4.0,<5.0',
]

setup(
    author='Jonas Ohrstrom',
    author_email='ohrstrom@gmail.com',
    url='https://github.com/digris/odr-stream-router',
    name='odroute',
    version='0.0.8',
    description='A primitive tool to route streams from ord-dabmod',
    packages=find_packages(),
    install_requires=INSTALL_REQUIREMENTS,
    entry_points='''
        [console_scripts]
        odroute=odroute:cli
    ''',
)
