#! /usr/bin/env python
#############################################################
#     File Name           :     setup.py
#     Created By          :     Ye Chang
#     Creation Date       :     [2017-10-05 13:52]
#     Last Modified       :     [2017-10-05 21:35]
#     Description         :
#############################################################

import os
from setuptools import setup, find_packages, Command

import fqutils


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """delete the build and sdist files"""
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


print(
find_packages('.', exclude=('tests*', 'docs', 'contrib'))
)

setup(
    name=fqutils.__title__,
    version=fqutils.__version__,
    description=fqutils.__description__,
    long_description=open("README.rst").read(),
    license=fqutils.__license__,
    url=fqutils.__url__,
    author=fqutils.__author__,
    author_email=fqutils.__email__,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires='>=3.5',
    packages=['fqutils'],
    # packages=find_packages('.', exclude=('tests*', 'docs', 'contrib')),
    install_requires=['pygatb', 'eta'],
    # package_dir={'': 'src'},  # tell distutils packages are under src
    # package_data={
    # If any package contains *.txt files, include them:
    # '': ['*.txt'],
    # And include any *.dat files found in the 'data' subdirectory
    # of the 'mypkg' package, also:
    # 'mypkg': ['data/*.dat'],
    # }
    cmdclass={
        'clean': CleanCommand,
    })
