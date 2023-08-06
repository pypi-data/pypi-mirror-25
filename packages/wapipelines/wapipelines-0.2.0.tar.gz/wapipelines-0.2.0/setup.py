#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')

with open('requirements-dev.txt') as req_file:
    requirements_dev = req_file.read().split('\n')

with open('VERSION') as fp:
    version = fp.read().strip()

setup(
    name='wapipelines',
    version=version,
    description="WA Pipelines",
    long_description=readme,
    author="Simon de Haan",
    author_email='simon@praekelt.org',
    url='https://github.com/praekeltfoundation/wa-pipelines',
    packages=[
        'wapipelines',
    ],
    package_dir={'wapipelines':
                 'wapipelines'},
    extras_require={
        'dev': requirements_dev,
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='wa-pipelines',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
