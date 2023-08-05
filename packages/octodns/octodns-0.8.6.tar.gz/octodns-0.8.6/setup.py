#!/usr/bin/env python

from os.path import dirname, join
import octodns

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

cmds = (
    'compare',
    'dump',
    'report',
    'sync',
    'validate'
)
cmds_dir = join(dirname(__file__), 'octodns', 'cmds')
console_scripts = {
    'octodns-{name} = octodns.cmds.{name}:main'.format(name=name)
    for name in cmds
}

setup(
    author='Ross McFarland',
    author_email='rwmcfa1@gmail.com',
    description=octodns.__doc__,
    entry_points={
        'console_scripts': console_scripts,
    },
    install_requires=[
        'PyYaml>=3.12',
        'dnspython>=1.15.0',
        'futures>=3.0.5',
        'incf.countryutils>=1.0',
        'ipaddress>=1.0.18',
        'natsort>=5.0.3',
        'python-dateutil>=2.6.0',
        'requests>=2.13.0'
    ],
    license='MIT',
    long_description=open('README.md').read(),
    name='octodns',
    packages=find_packages(),
    url='https://github.com/github/octodns',
    version=octodns.__VERSION__,
)
