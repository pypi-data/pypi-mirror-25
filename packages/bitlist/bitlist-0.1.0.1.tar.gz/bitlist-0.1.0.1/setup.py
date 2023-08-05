from setuptools import setup

setup(
    name             = 'bitlist',
    version          = '0.1.0.1',
    packages         = ['bitlist',],
    install_requires = [],
    license          = 'MIT',
	url              = 'https://github.com/lapets/bitlist',
	author           = 'Andrei Lapets',
	author_email     = 'a@lapets.io',
    description      = 'Minimal Python library for working with little-endian list representation of bit strings.',
    long_description = open('README.rst').read(),
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
)
