#!/usr/bin/env python3

from setuptools import (
    setup,
    find_packages,
)
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

from compile import copy_build_templates

VERSION = '0.1.1'


class EggInfoCommand(egg_info):

    def run(self):
        copy_build_templates()
        egg_info.run(self)


class InstallCommand(install):

    def run(self):
        copy_build_templates()
        install.run(self)


class DevelopCommand(develop):

    def run(self):
        copy_build_templates()
        develop.run(self)


setup(
    name='paperify',
    version=VERSION,
    description="Make beautiful documents, fast.",
    long_description=open('README.md').read(),
    author='Seb Arnold',
    author_email='smr.arnold@gmail.com',
    url='http://www.seba1511.com',
    download_url='https://github.com/seba-1511/paperify/archive/' + VERSION + '.zip',
    license='License :: OSI Approved :: Apache Software License',
    packages=find_packages(exclude=["tests"]),
    classifiers=[],
    cmdclass={
        'install': InstallCommand,
        'develop': DevelopCommand,
    },
    install_requires=[open('requirements.txt').read().split('\n')],
    scripts=[
        'bin/paperify.py',
    ]
)
