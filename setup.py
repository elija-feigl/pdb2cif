#!/usr/bin/env python
# Copyright (C) 2021-Present  Elija Feigl
# Full GPL-3 License can be found in `LICENSE` at the project root.
""" PDB file to mmCIF file conversion script."""
from setuptools import find_packages
from setuptools import setup


setup(
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        pdb2cif=pdb2cif.scripts.pdb2cif:cli
    """,
)
