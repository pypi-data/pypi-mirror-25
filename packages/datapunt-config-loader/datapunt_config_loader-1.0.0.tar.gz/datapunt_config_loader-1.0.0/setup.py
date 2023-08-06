#!/usr/bin/env python
"""See <https://setuptools.readthedocs.io/en/latest/>.
"""
from setuptools import setup, find_packages

tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-aiohttp',
]

setup(

    # ┏━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ Publication Metadata ┃
    # ┗━━━━━━━━━━━━━━━━━━━━━━┛
    version='1.0.0',
    name='datapunt_config_loader',
    description="Loads Yaml configuration files",
    long_description="""
        This package helps you read your application’s configuration from a YAML
        file.  It provides:

        -   schema validation of your configuration file
        -   variable interpolation using environment variables.

    """,
    url='https://github.com/Amsterdam/config_loader',
    author='Amsterdam City Data',
    author_email='datapunt@amsterdam.nl',
    license='Mozilla Public License Version 2.0',
    classifiers=[
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],


    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ Packages and package data ┃
    # ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
        'config_loader': ['schema_example.yaml', 'config_example.yaml']
    },


    # ┏━━━━━━━━━━━━━━┓
    # ┃ Requirements ┃
    # ┗━━━━━━━━━━━━━━┛
    python_requires='~=3.6',
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'jsonschema',
        'PyYaml',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
)
