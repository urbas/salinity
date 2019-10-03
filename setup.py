#!/usr/bin/env python

from setuptools import setup, find_packages

REQUIREMENTS = ["click>=7.0"]

SETUP_REQUIREMENTS = ["pytest-runner"]

TEST_REQUIREMENTS = ["pytest"]

with open("README.md", "r") as fh:
    readme = fh.read()

with open("RELEASE_NOTES.md", "r") as fh:
    release_notes = fh.read()

setup(
    author_email="matej.urbas@gmail.com",
    author="Matej Urbas",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
    description="Analyzes Salt's highstate output and produces a report.",
    entry_points={"console_scripts": ["salinity=salinity.app:main"]},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    keywords="salinity",
    long_description_content_type="text/markdown",
    long_description=readme + "\n\n" + release_notes,
    name="salinity",
    packages=find_packages(include=["salinity"]),
    setup_requires=SETUP_REQUIREMENTS,
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    url="https://github.com/urbas/salinity",
    version="0.1.3",
)
