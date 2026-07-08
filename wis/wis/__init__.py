"""Top-level package for wis.py."""

import logging

from .wis import Wis

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = """Matthew John Payne"""
__email__ = "mpayne@cfa.harvard.edu;matthewjohnpayne@gmail.com"
__version__ = "2.0.0"
__all__ = ["Wis"]
