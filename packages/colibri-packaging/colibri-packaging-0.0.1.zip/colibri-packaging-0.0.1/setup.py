# coding: utf-8
from setuptools import setup
try:
    from versao import versao_lib
except ImportError:
    versao_lib = '0.0'


setup(
    name='colibri-packaging',
    author='Colibri Agile',
    author_email='colibri.agile@gmail.com',
    platforms=['Windows'],
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html'
    version=versao_lib,
    description='Colibri Master Packages generator',
    packages=[
        'colibri-packaging'
    ],
    package_data={
        'colibri-packaging': ['7za.exe']
    },
    data_files=[('', 'LICENSE.txt')],
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    python_requires='2.7'
)
