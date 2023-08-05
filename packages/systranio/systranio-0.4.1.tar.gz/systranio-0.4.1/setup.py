"""
Setup script

`pypandoc` is recommended to convert README.md to restructuredText
if it’s missing systranio’s page on PyPi is gonna be a bit ugly

Usage :
* `python setup.py sdist upload` -> build & upload
* `python setup.py test -> run unittests
"""

from setuptools import setup, find_packages

try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    print('!!! pandoc is missing, long_description’s body will in markdown')
    README = open('README.md').read()

REQUIRES = ['requests >= 2']

setup(
    name='systranio',
    version='0.4.1',  # managed by bumbversion
    description='A simple REST API client for Systran.io',
    author='Canarduck',
    author_email='renaud@canarduck.com',
    url='https://gitlab.com/canarduck/systranio',
    keywords='api rest systran translation',
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha', 'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ],
    test_suite='tests')
