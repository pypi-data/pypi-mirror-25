# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name = 'pyLearnstimate',
    packages = ['pyLearnstimate'], # this must be the same as the name above
    version = '0.1',
    description = 'Machine learning for optimal estimation',
    author = 'Sasha Petrenko',
    author_email = 'sap625@mst.edu',
    url = 'https://gitlab.com/ap6yc/ap6yc.gitlab.io', # use the URL to the github repo
    license='MIT',
    keywords = ['testing', 'logging', 'example'], # arbitrary keywords
    classifiers = [],
    install_requires=['networkx','numpy','scipy'],
)
