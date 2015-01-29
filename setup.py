#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements
from pip.download import PipSession

import bughouse

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = bughouse.__version__

readme = open('README.rst').read()

requirements = [str(req.req) for req in parse_requirements('requirements.txt', session=PipSession())]

setup(
    name='Bughouse Rankings',
    version=version,
    description="""Rankings for our bughouse games""",
    long_description=readme,
    author='Piper Merriam',
    author_email='piper@simpleenergy.com',
    url='https://github.com/simpleenergy/bughouse-rankings',
    packages=[
        'bughouse',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='bughouse-rankings',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
