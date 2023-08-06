#! /usr/bin/env python3

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='markdown-figure',
    version='0.0.1',

    author='Jan Willhaus',
    author_email='mail@janwillhaus.de',

    description='Markdown extension which turns images into figures',
    long_description=long_description,

    url='https://github.com/janwh/markdown-figures',
    license='MIT',
    keywords='markdown extension html figure',

    py_modules=['mdfigure'],
    install_requires=['Markdown>=2.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)
