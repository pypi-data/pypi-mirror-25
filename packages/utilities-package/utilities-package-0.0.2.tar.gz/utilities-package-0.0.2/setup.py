# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import setup

setup(
    name='utilities-package',
    version='0.0.2',
    description='utilities package',
    url='https://github.com/terminal-labs/utilities',
    author='Michael Verhulst',
    author_email='michael@terminallabs.com',
    license="license",
    packages=['utilities'],
    zip_safe=False,
    install_requires=['bash'],
    )
