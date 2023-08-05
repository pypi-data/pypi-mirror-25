# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='filework',
    version='1.1.0',
    description='A simple wrapper class for easy reading from/iterating through, writing, and appending to files.',
    long_description=long_description,
    url='https://github.com/aescwork/filework',
    author='aescwork',
    author_email='aescwork@protonmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
		'Topic :: System :: Filesystems',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='filework development files file read write delete append',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={
        'filework': ['package_data.dat'],
    },
    entry_points={
        'console_scripts': [
            'filework=filework:main',
        ],
    },
)
