#!/usr/bin/env python
# Copyright (C) 2021-Present  Elija Feigl
# Full GPL-3 License can be found in `LICENSE` at the project root.
""" PDB file to mmCIF file conversion script module:"""
import logging
from pathlib import Path
from typing import List

import click
from pdb2cif import __version__
from pdb2cif.pdb.structure import Structure

logger = logging.getLogger(__name__)


def print_version(ctx, _, value):
    """click print version."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option("--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    """
    PDB file to mmCIF file conversion
    """


@cli.command()
@click.argument("pdb", type=click.Path(exists=True, resolve_path=True, path_type=Path))
@click.option("--remove-H", "remove_h", is_flag=True, help="remove hydrogen atoms")
@click.option("--snupi", "is_snupi", is_flag=True, help="convert from SNUPI pdb")
@click.option(
    "--flip-fields",
    "flip_fields",
    is_flag=True,
    help="flip the values of occupancy and temperature",
)
def pdb2cif(pdb, remove_h, is_snupi, flip_fields):
    """convert atomic model in mmCIF format from namd PDB

    PDB is the name of the namd configuration file [.pdb]\n
    """
    _check_path(pdb, [".pdb"])
    structure = Structure(path=pdb, remove_H=remove_h, is_snupi=is_snupi, flip_fields=flip_fields)
    structure.parse_pdb()
    # TODO-low: ask for additional info (name, author, etc)
    output_name = pdb.with_suffix(".cif")
    structure.write_cif(output_name)


def _check_path(filepath: Path, extensions: List[str]):
    if filepath.suffix not in extensions:
        raise Exception(f"input file {filepath} does not have correct extension {extensions}")
