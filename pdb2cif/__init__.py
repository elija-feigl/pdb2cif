#!/usr/bin/env python
# Copyright (C) 2021-Present  Elija Feigl
# Full GPL-3 License can be found in `LICENSE` at the project root.
import logging
import os
from pathlib import Path


def get_version() -> str:
    return __version__


def get_resource(resources: str) -> Path:
    return Path(__file__).parent / "resources" / resources


def _init_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | [%(module)s]\t%(levelname)s\t- %(message)s", "%Y.%m.%d %H:%M"
    )
    handler.setFormatter(formatter)

    if os.name != "nt":  # no ANSI escape support on Windows
        logging.addLevelName(
            logging.WARNING, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.WARNING)
        )
        logging.addLevelName(
            logging.ERROR, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.ERROR)
        )
        logging.addLevelName(
            logging.CRITICAL, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL)
        )
    logger.addHandler(handler)


_init_logging()

version_info = [1, 0, 5]

__version__ = ".".join([str(sub) for sub in version_info])
__all__ = ["__version__"]
