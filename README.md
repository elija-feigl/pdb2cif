[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python-version:](https://img.shields.io/badge/python-v3.8-green)]() | [Dependencies](#dependencies) | [Installation](#installation) | [Usage](#usage)


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
  see setup.cfg

## Installation
  ```
    git clone https://github.com/elija-feigl/pdb2cif
    cd pdb2cif
    pip install .
  ```
or
  ```
    pip install git+https://github.com/elija-feigl/pdb2cif#egg=pdb2cif
  ```

## Usage
```
pdb2cif [OPTIONS] PDB

  Generate atomic model in mmCIF format from namd PDB.
    PDB is the name of the namd configuration file [.pdb]

Options:
  -h, --help     Show this message and exit.
  -v, --version  Show __version__ and exit.
  
  --remove-H     Remove hydrogen atoms.
  --snupi        Convert from SNUPI pdb.
  --flip-fields  Flip the values of occupancy and temperature fields.

```