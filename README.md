[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python-version:](https://img.shields.io/badge/python-v3.8-green)]() | [Dependencies](#dependencies) | [Installation](#installation)


# Disclaimer
 this repository is a standalone for the pdb utility of dnaFit
 please report issues at: https://github.com/elija-feigl/dnaFit


# pdb2cif

A Python3 PDB to mmCIF conversion tool.
Intended for internal use at Dietzlab, TUM Munich
This tools enables usage of atomic coordinate files with chimera and chimeraX

Supported Sources:
  * mrdna
  * tacoxDNA
  * SNUPI


## Dependencies

* Python >= 3.8
  see requiremets.txt

## Installation

    git clone https://github.com/elija-feigl/pdb2cif
    cd pdb2cif
    python setup.py install
