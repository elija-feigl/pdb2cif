#!/usr/bin/env python
# Copyright (C) 2021-Present  Elija Feigl
# Full GPL-3 License can be found in `LICENSE` at the project root.
from dataclasses import dataclass
from dataclasses import field
import logging
from pathlib import Path
from typing import List
from typing import Tuple

from .atom import Atom
from .files import CIF
from .files import PDB


@dataclass
class Structure:
    path: Path
    remove_H: bool = True
    is_snupi: bool = False
    alt_chain_id: bool = False
    flip_fields: bool = False

    atoms: List[Atom] = field(default_factory=list)
    # TODO-IMPROVEMENT: defaults and other attributes: sequences etc

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        self.name = self.path.stem  # TODO-IMPROVEMENT pass name option
        self.keep_resID: bool = True
        self.previous_atm: Tuple[str, int] = ("", 0)
        self.previous_res: Tuple[str, int] = ("", 0)
        self.previous_chain: Tuple[str, int, bool] = ("", 0, True)  # str, int, new

    def add_atom(self, atom: Atom) -> None:
        self.atoms.append(atom)

    def _parse_cif_info(self):
        raise NotImplementedError

    def _parse_cif_atom(self):
        raise NotImplementedError

    def parse_cif(self) -> None:
        self._parse_cif_info()
        self._parse_cif_atom()
        raise NotImplementedError

    def _parse_pdb_info(self, _: str):
        # TODO-IMPROVEMENT: collect extra data
        return

    def _eval_atm_number(
        self,
        string: str,
    ) -> int:
        atm_number = self.previous_atm[1] + 1
        self.previous_atm = (string, atm_number)
        return atm_number

    def _eval_res_number(self, string: str) -> int:
        string = string.strip()
        if self.is_snupi:
            res_number = int(string)
            if res_number < self.previous_res[1]:
                res_number = 1
            elif res_number != self.previous_res[1]:
                res_number = self.previous_res[1] + 1
        elif string.isdigit() and self.keep_resID:
            res_number = int(string)
        else:
            self.keep_resID = False
            if string == self.previous_res[0]:
                res_number = self.previous_res[1]
            else:
                res_number = self.previous_res[1] + 1

        if res_number == 1 and self.previous_res[1] != 1:
            self.previous_chain = (self.previous_chain[0], self.previous_chain[1], True)
        self.previous_res = (string, res_number)
        return res_number

    def _eval_chain_id(self, string: str) -> int:
        if string != self.previous_chain[0] or self.previous_chain[2]:
            chain_id = self.previous_chain[1] + 1
            self.previous_chain = (string, chain_id, False)
        else:
            chain_id = self.previous_chain[1]
        return chain_id

    def _parse_pdb_atom(self, line: str) -> None:

        def _test_validity(i_atom_coor: List[str], line: str) -> None:
            _ = [float(c) for c in i_atom_coor]
            _ = float(line[54:59].strip())
            _ = float(line[59:66].strip())

        def _parse_alt_shift(line: str) -> Tuple[int, int]:
            coords = line[30 : 54 + 6]
            i_atom_coor = []
            coor, n_decimal = "", 0
            max_char = 0
            for max_char, char in enumerate(coords):
                if char in ["-", " "] and coor != "" or n_decimal == 3:
                    i_atom_coor.append(coor)
                    coor, n_decimal = "", 0
                if char.isdigit() or char in ["-", "."]:
                    coor += char
                    if "." in coor and char.isdigit():
                        n_decimal += 1
                if len(i_atom_coor) == 3:
                    _alt_shift = max_char - 22
                    return _alt_shift, i_atom_coor
            return 0, i_atom_coor

        atom_name = line[12:16]
        if "H" in atom_name and self.remove_H:
            return
        atm_number = self._eval_atm_number(line[6:11])
        res_number = self._eval_res_number(line[22:28])

        i_atom_coor = [line[30:38], line[38:46], line[46:54]]
        _alt_shift = 0
        try:
            _test_validity(i_atom_coor, line)
        except ValueError:
            _alt_shift, i_atom_coor = _parse_alt_shift(line)

        try:
            _ = [float(c) for c in i_atom_coor]
        except ValueError:
            raise ValueError(f"Error parsing atom coordinates: {i_atom_coor}")

        opacity = line[54 + _alt_shift : 59 + _alt_shift].strip()
        temperature = line[59 + _alt_shift : 66 + _alt_shift].strip()
        str_chain_id = line[72 + _alt_shift : 78 + _alt_shift] if self.alt_chain_id else line[20:22]
        chain_id = self._eval_chain_id(str_chain_id.strip())

        if self.flip_fields:
            opacity, temperature = temperature, opacity

        self.add_atom(
            Atom(
                i_atom_coor=i_atom_coor,
                i_atom_number=atm_number,
                i_atom_name=atom_name,
                i_res_name=line[17:20],
                i_chain_id=chain_id,
                i_res_number=res_number,
                i_opacity=opacity,
                i_temperature=temperature,
            )
        )

    def _parse_pdb_generate_info(self):
        # generate sequences etc
        raise NotImplementedError

    def parse_pdb(self) -> None:
        self.logger.info("Parsing pdb file: %s", self.path)
        with self.path.open(mode="r") as fi:
            for line in fi.readlines():
                lineType = line[0:6].strip()
                if lineType == "ATOM":
                    self._parse_pdb_atom(line)
                else:
                    self._parse_pdb_info(line)

        # TODO-IMPROVEMENT: generate implicit data: sequences
        # self._parse_pdb_generate_info()

    def write_pdb(self, outfile: Path) -> None:
        pdb = PDB(struct=self)
        pdb.write(outfile=outfile)

    def write_cif(self, outfile: Path) -> None:
        # generate sequences here (from atom)
        cif = CIF(struct=self)
        self.logger.info("Writing new mmCif file: %s", outfile)
        cif.write(outfile=outfile)
