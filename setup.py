from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(

    name='anthill',

    version='1.0',
    description='A compendium of useful python libraries',
    long_description=read('README.md'),

    author='stealthizer',
    author_email='stealthizer',

    url='https://github.com/stealthizer/anthill',

    classifiers=[

        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],

    packages=find_packages(),
)
