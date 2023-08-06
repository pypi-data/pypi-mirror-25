# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='sphinx-guillotina-theme',
    version='1.0.0',
    description='sphinx theme for guillotina',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    keywords=['sphinx', 'theme', 'guillotina'],
    author='Nathan Van Gheem',
    author_email='vangheem@gmail.com',
    classifiers=[
    ],
    url='https://github.com/guillotinaweb/sphinx-guillotina-theme',
    license='BSD',
    setup_requires=[
    ],
    zip_safe=True,
    include_package_data=True,
    package_data={'': ['*.txt', '*.rst', 'guillotina/documentation/meta/*.json']},
    packages=find_packages(),
    install_requires=[
        'sphinx'
    ]
)
