#!/usr/bin/env python
from setuptools import setup


setup(
    name='skywise-platform',
    version='0.1.7',
    package_data={'': ['README.md']},
    packages=['skywiseplatform'],
    install_requires=[
        'skywise-rest-client>=1.0.7',
        'voluptuous>=0.8.8'
    ],

    # metadata for upload to PyPI
    author='Weather Decision Technologies',
    author_email='jstewart@wdtinc.com',
    description='SkyWise Platform API Python Client Library',
    url='https://github.com/wdtinc/skywise-platform-py',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    )
)
