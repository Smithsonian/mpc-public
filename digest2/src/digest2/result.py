"""Dataclasses for digest2 classification results."""

from dataclasses import dataclass, fields


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
