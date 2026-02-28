"""
digest2 — NEO orbit classification from short-arc astrometric tracklets.

This package provides Python bindings to the digest2 orbit classification
engine, which uses statistical ranging techniques on short-arc astrometry
to compute probabilities that observed objects belong to various orbit classes.

Quick start::

    from digest2 import Digest2

    d2 = Digest2()
    results = d2.classify_file("observations.obs")
    for r in results:
        print(r.designation, r.noid.NEO)
    d2.close()

Or as a one-shot::

    from digest2 import classify
    result = classify("observations.obs")
"""

from digest2.core import Digest2, classify
from digest2.observation import Observation, parse_mpc80, parse_mpc80_file
from digest2.population import build_model, read_model_csv
from digest2.result import ClassificationResult, Scores
from digest2.truth import (
    GroundTruthRecord,
    MatchedResult,
    TruthEvaluator,
    classify_orbit,
    classify_orbit_all,
    load_ground_truth,
    load_trksub_mapping,
)

__all__ = [
    "Digest2",
    "classify",
    "ClassificationResult",
    "Scores",
    "Observation",
    "parse_mpc80",
    "parse_mpc80_file",
    "build_model",
    "read_model_csv",
    "GroundTruthRecord",
    "MatchedResult",
    "TruthEvaluator",
    "classify_orbit",
    "classify_orbit_all",
    "load_ground_truth",
    "load_trksub_mapping",
]
