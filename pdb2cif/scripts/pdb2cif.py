#!/usr/bin/env python
# Copyright (C) 2021-Present  Elija Feigl
# Full GPL-3 License can be found in `LICENSE` at the project root.
""" PDB file to mmCIF file conversion script module:"""
import logging
from pathlib import Path
import sys
from typing import List

import click
from pdb2cif import get_version
from pdb2cif.pdb.structure import Structure

logger = logging.getLogger(__name__)


def print_version(ctx, _, value):
    """click print version."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(get_version())
    ctx.exit()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("pdb", type=click.Path(exists=True, resolve_path=True, path_type=Path))
@click.option(
    "-v",
    "--version",
    is_flag=True,
    help="Show __version__ and exit.",
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@click.option("--remove-H", "remove_h", is_flag=True, help="Remove hydrogen atoms.")
@click.option("--snupi", "is_snupi", is_flag=True, help="Convert from SNUPI pdb.")
@click.option(
    "--flip-fields",
    "flip_fields",
    is_flag=True,
    help="Flip the values of occupancy and temperature fields.",
)
def pdb2cif(pdb, remove_h, is_snupi, flip_fields):
    """\b
    Generate atomic model in mmCIF format from namd PDB.
    \b
    PDB is the name of the namd configuration file [.pdb]
    """
    logger.info("pdb2cif version: %s", get_version())
    _check_path(pdb, [".pdb"])
    structure = Structure(path=pdb, remove_H=remove_h, is_snupi=is_snupi, flip_fields=flip_fields)
    structure.parse_pdb()
    # TODO-IMPROVEMENT: ask for additional info (name, author, etc)
    output_name = pdb.with_suffix(".cif")
    structure.write_cif(output_name)


def _check_path(filepath: Path, extensions: List[str]):
    if filepath.suffix not in extensions:
        logger.critical("Input file %s does not have correct extension %s.", filepath, extensions)
        sys.exit(1)
