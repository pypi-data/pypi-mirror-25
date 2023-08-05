from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="extend_Library",
    version="1.0.0",
    author="SRTest",
    author_email="liuhy@emrubik.com",
    description="Extend library for EMP.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/desion/tidy_page",
    packages=['extend_Library'],
    install_requires=[
        "beautifulsoup4",
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)