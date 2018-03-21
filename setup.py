# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='console_log',
    version='0.1.0',
    description='Log to browser console',
    long_description=readme,
    author='Beto Dealmeida',
    author_email='beto@lyft.com',
    url='https://github.com/betodealmeida/consolelog',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['werkzeug'],
)
