# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

# version
here = os.path.dirname(os.path.abspath(__file__))

setup(
    name='flachemy-session',
    version='0.0.3',
    author='ksk_uchi',
    author_email='ksk.uchi+flachemy-session@gmail.com',
    maintainer='kinpira',
    maintainer_email='ksk.uchi+flachemy-session@gmail.com',
    description='Ease to handle sqlalchemy session with flask.',
    long_description=readme,
    packages=find_packages(),
    install_requires=['Flask>=0.12', 'SQLAlchemy>=1.1.10'],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
