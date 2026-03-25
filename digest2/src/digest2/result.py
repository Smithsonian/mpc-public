"""Dataclasses for digest2 classification results."""

from dataclasses import dataclass, field, fields
from typing import Optional, Tuple


@dataclass(frozen=True)
class Scores:
    """Scores for each orbit class (0-100).

    Attributes correspond to the 15 orbit classes used by digest2.
    Supports both attribute access (``scores.NEO``) and dict-style
    access (``scores["NEO"]``) for convenience.
    """

    Int: float = 0.0
    NEO: float = 0.0
    N22: float = 0.0
    N18: float = 0.0
    MC: float = 0.0
    Hun: float = 0.0
    Pho: float = 0.0
    MB1: float = 0.0
    Pal: float = 0.0
    Han: float = 0.0
    MB2: float = 0.0
    MB3: float = 0.0
    Hil: float = 0.0
    JTr: float = 0.0
    JFC: float = 0.0

    def __getitem__(self, key: str) -> float:
        """Allow dict-style access: ``scores["NEO"]``."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def items(self):
        """Iterate over (abbreviation, score) pairs."""
        return ((f.name, getattr(self, f.name)) for f in fields(self))

    def __iter__(self):
        """Iterate over class abbreviations."""
        return (f.name for f in fields(self))


@dataclass(frozen=True)
class TrialOrbit:
    """A single trial orbit generated during statistical ranging.

    Attributes:
        q: Perihelion distance (AU).
        e: Eccentricity.
        i: Inclination (degrees).
        H: Absolute magnitude.
        d: Geocentric distance used to generate this orbit (AU).
        an: Angle parameter used in orbit solution (radians).
        iq: q bin index (0..28).
        ie: e bin index (0..7).
        ii: i bin index (0..10).
        ih: H bin index (0..17).
        new_tag: True if this orbit tagged a previously unvisited bin.
    """

    q: float
    e: float
    i: float
    H: float
    d: float
    an: float
    iq: int
    ie: int
    ii: int
    ih: int
    new_tag: bool


@dataclass(frozen=True)
class ClassificationResult:
    """Result of classifying a single tracklet.

    Attributes:
        raw: Raw population scores for each orbit class.
        noid: NoID scores (accounting for known objects) for each class.
        rms: Great-circle RMS fit of the tracklet in arcseconds.
        rms_prime: RMS prime value from ADES uncertainties.
        designation: Object designation (populated by ``classify_file``).
    """

    raw: Scores
    noid: Scores
    rms: float
    rms_prime: float
    designation: str = ""
    trial_orbits: Optional[Tuple[TrialOrbit, ...]] = None
    _orbit_elements_cache: Optional[dict] = field(
        default=None, init=False, repr=False, compare=False
    )

    @property
    def top_class(self) -> str:
        """Return the class abbreviation with the highest NoID score."""
        best_abbr = "Int"
        best_val = -1.0
        for abbr, val in self.noid.items():
            if val > best_val:
                best_val = val
                best_abbr = abbr
        return best_abbr

    @property
    def orbit_elements(self) -> Optional[dict]:
        """Return trial orbit elements as a dict of numpy arrays.

        Returns None if trial_orbits were not collected. Otherwise returns
        a dict with keys: 'q', 'e', 'i', 'H', 'd', 'an', 'iq', 'ie',
        'ii', 'ih', 'new_tag', each mapping to a numpy array.
        """
        if self.trial_orbits is None:
            return None

        if self._orbit_elements_cache is not None:
            return self._orbit_elements_cache

        import numpy as np

        n = len(self.trial_orbits)
        result = {
            "q": np.empty(n, dtype=np.float64),
            "e": np.empty(n, dtype=np.float64),
            "i": np.empty(n, dtype=np.float64),
            "H": np.empty(n, dtype=np.float64),
            "d": np.empty(n, dtype=np.float64),
            "an": np.empty(n, dtype=np.float64),
            "iq": np.empty(n, dtype=np.int32),
            "ie": np.empty(n, dtype=np.int32),
            "ii": np.empty(n, dtype=np.int32),
            "ih": np.empty(n, dtype=np.int32),
            "new_tag": np.empty(n, dtype=np.bool_),
        }
        for j, orb in enumerate(self.trial_orbits):
            result["q"][j] = orb.q
            result["e"][j] = orb.e
            result["i"][j] = orb.i
            result["H"][j] = orb.H
            result["d"][j] = orb.d
            result["an"][j] = orb.an
            result["iq"][j] = orb.iq
            result["ie"][j] = orb.ie
            result["ii"][j] = orb.ii
            result["ih"][j] = orb.ih
            result["new_tag"][j] = orb.new_tag
        object.__setattr__(self, "_orbit_elements_cache", result)
        return result
