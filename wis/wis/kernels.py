"""Predefined WIS kernels.

This module exports the built-in KernelSpecifier objects for convenient use.
Users can import these directly when instantiating Wis or creating custom kernel configurations.

Examples:
    >>> from wis.kernels import DE430
    >>> with Wis(kernels=DE430) as w:
    ...     # Only DE430 kernel loaded

    >>> from wis.kernels import DE430, TESS
    >>> with Wis(kernels=[DE430, TESS]) as w:
    ...     # DE430 ground kernel and TESS satellite kernel loaded

    >>> from wis.kernels import DE430
    >>> from my_module import MyCustomKernel
    >>> with Wis(kernels=[DE430, MyCustomKernel]) as w:
    ...     # Mix built-in and custom kernels

Available kernels:
    DE430: Ground-based observatories using DE430 ephemeris
    DE440: Ground-based observatories using DE440 ephemeris
    KEPLER: Kepler/K2 satellite
    TESS: TESS satellite
    GAIA: Gaia spacecraft
    HST: Hubble Space Telescope
    JWST: James Webb Space Telescope
"""

from wis.kernel_instances_ground import DE430, DE440
from wis.kernel_instances_satellites import (
    GAIA,
    HST,
    JWST,
    KEPLER,
    TESS,
)

__all__ = [
    "DE430",
    "DE440",
    "GAIA",
    "HST",
    "JWST",
    "KEPLER",
    "TESS",
]
