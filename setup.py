from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(

    name='vibbo-devops--libs',

    version='1.0',

    description='Python tools for deploy and maintenance',
    long_description=read('README.md'),

    author='Schibsted Spain devops vibbo',
    author_email='dev.ops.vibbo@scmspain.com',

    url='https://github.schibsted.io/scmspain/devops-vibbo--libs',

    classifiers=[

        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
