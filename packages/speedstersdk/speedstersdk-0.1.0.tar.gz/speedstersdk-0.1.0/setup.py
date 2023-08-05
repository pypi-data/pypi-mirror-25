# -*- coding: utf-8 -*-

u"""
(c) Copyright 2016 Telefónica I+D. Printed in Spain (Europe). All Rights
Reserved.
The copyright to the software program(s) is property of Telefónica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefónica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
"""

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

VERSION = '0.1.0'

packages = [
    'speedstersdk',
    'speedstersdk.insight',
    'speedstersdk.dormer',
    'speedstersdk.processor',
]


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=PipSession())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')

except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='speedstersdk',
    version=VERSION,
    description='Speedster SDK.',
    long_description=read_md,
    author='SmartDigits Team',
    author_email='jetsetme@tid.es',
    url='http://www.smartdigits.io',
    packages=packages,
    package_data={'': ['*.md']},
    include_package_data=True,
    install_requires=reqs,
    license='Apache 2.0',
    zip_safe=True,
)
