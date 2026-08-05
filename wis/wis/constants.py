"""This file contains various constants & parameters used throughout the wis.py codebase.

This includes physical constants, directories, and ... nothing else at the moment.
"""

import os
from dataclasses import dataclass
from enum import StrEnum

import astropy.units as u


class AllowedDEs(StrEnum):
    """Allowed Ephemeris Choices."""

    DE430 = "DE430"
    DE440 = "DE440"


@dataclass
class PhysicalConstants:
    """Float values of physical constants used throughout the codebase."""

    # note: u.R_earth.to(u.km) gives 6378.1km, but presumably we care about those 30m
    Rearth_km: float = (
        6378.1363  # Handled by pck00011.tpc [e.g. https://spiceypy.readthedocs.io/en/stable/other_stuff.html]
    )
    au_km: float = u.au.to(u.km)
    Rearth_AU: float = Rearth_km / au_km
    day_s: float = 86400


# Directories
# --------------------------------------------------------------------------
class Directories:
    """Handle the directories where data is stored and loaded from."""

    # By default, all data is stored in a hidden directory in the user's home directory
    # - Change this if desired
    data_dir = os.path.join(os.path.expanduser("~"), ".wispykernels")

    def __init__(
        self,
    ) -> None:
        """Initialize the Directories class and create the data directory if it doesn't exist."""
        os.makedirs(self.data_dir, exist_ok=True)

    def obscode_data_subdir(self, obscode: str) -> str:
        """Returns the path to the subdirectory where files will be saved or loaded for a specific obscode."""
        subdir = os.path.join(self.data_dir, obscode)
        os.makedirs(subdir, exist_ok=True)
        return subdir
