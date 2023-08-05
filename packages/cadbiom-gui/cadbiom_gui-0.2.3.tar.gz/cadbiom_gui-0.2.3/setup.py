#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017  IRISA
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# The original code contained here was initially developed by:
#
#     Geoffroy Andrieux.
#     IRISA/IRSET
#     Symbiose team
#     IRISA  Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE
#
#
# Contributor(s): Michel Le Borgne, Nolwenn Le Meur, Pierre Vignet

"""Definition of setup function for setuptools module."""

# Standard imports
from setuptools import setup, find_packages

__PACKAGE_VERSION__ = "0.2.3"
__LIBRARY_VERSION__ = "0.1.0"

setup(

    # Library name & version
    name='cadbiom_gui',
    version=__PACKAGE_VERSION__,

    # Search all packages recursively
    packages=find_packages(),

    # Authors
    author="pvignet",
    author_email="pierre.vignet@irisa.fr",

    # Description
    description="GUI tool for the Cadbiom library",
    long_description=open('README.md').read(),

    # MANIFEST.in ?
    include_package_data=True,

    # Official page
    url = "https://gitlab.irisa.fr/0000B8EG/Cadbiom/tree/pypi_packaging",

    # Metadata
    classifiers=[
        "Environment :: X11 Applications :: GTK",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: French",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],

    entry_points={
        'gui_scripts': ['cadbiom = cadbiom_gui.__main__:main'],
    },

    install_requires=["cadbiom", "pygraphviz"],
)
