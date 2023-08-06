#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
import modelpai

setup(
    name = "modelpai",
    version = modelpai.__version__,
    keywords = ("pai"),
    description = "upload models to pai for training and republishing",
    long_description = "upload models to pai for training and republishing.",
    license = "MIT Licence",

    url = "",
    author = "acelin",
    author_email = "chaohui.lch@alibaba-inc.com",

    packages = ['modelpai',"modelpai/oss"],
    package_data = {
    },
    include_package_data = True,
    platforms = "any",
    install_requires = ["click"],

    scripts = ['bin/modelpai']
    #entry_points = {
    #    'console_scripts': [
    #        'modelpai=modelpai:model_pai'
    #    ]
    #}
)

