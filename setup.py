import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(

    name='awscommonlib',

    version='1.1',
    description='A compendium of useful python libraries',
    long_description=read('README.md'),

    author='stealthizer',
    author_email='stealthizer',

    url='https://github.com/stealthizer/awscommonlib',

    classifiers=[

        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.4',
    ],

    packages=find_packages(),
)
