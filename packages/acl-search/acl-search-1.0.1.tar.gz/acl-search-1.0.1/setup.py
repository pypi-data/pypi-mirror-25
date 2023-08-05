#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Command, find_packages

long_description = """
acl-search is a Python utility to search through an ACL file to find intersecting destination IPs and return the full term.
"""

version = '1.0.1'

setup(
    name = 'acl-search',
    packages = find_packages(),
    version = version,
    license='MIT',
    description = 'Search through an ACL file to find intersecting destination IPs',
    long_description=long_description,
    author = 'Brandon Wagner',
    author_email = 'brandon@brandonwagner.info',
    maintainer = 'Brandon Wagner',
    maintainer_email = 'brandon@brandonwagner.info',
    url = 'https://github.com/bwagner5/acl-search',
    download_url = "https://github.com/bwagner5/acl-search/archive/%s.tar.gz"%(version),
    scripts = ['acl-search'],
    zip_safe = True,
    install_requires=['ipaddress','pyparsing'],
)
