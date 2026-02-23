"""High-level API for digest2 orbit classification.

This module provides the main user-facing interface: the Digest2 class
for stateful classification, and the classify() convenience function for
one-shot use.
"""

import math
from pathlib import Path
from typing import Dict, List, Optional, Union

from digest2 import _extension
from digest2.model import find_config_path, find_model_path, find_obscodes_path
from digest2.observation import (
    Observation,
    parse_ades_xml,
    parse_mpc80_file,
)
from digest2.result import ClassificationResult, Scores


def _parse_config_file(config_path: str) -> dict:
    """Parse an MPC.config file to extract per-site observatory errors.

    Returns dict with keys:
        'site_errors': dict mapping obscode str -> error in arcsec
        'default_obserr': float or None
        'repeatable': bool or None
        Other config flags as needed.
    """
    result = {
        "site_errors": {},
        "default_obserr": None,
        "repeatable": None,
        "no_threshold": None,
    }

    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line == "repeatable":
                result["repeatable"] = True
            elif line == "random":
                result["repeatable"] = False
            elif line == "noThreshold":
                result["no_threshold"] = True
            elif line.startswith("obserr"):
                # Format: obserrXXX=Y.YY  where XXX is obscode, Y.YY is arcsec
                rest = line[6:]  # strip "obserr"
                if "=" in rest:
                    code, val = rest.split("=", 1)
                    code = code.strip()
                    val = val.strip()
                    try:
                        err_val = float(val)
                        if code:
                            result["site_errors"][code] = err_val
                        else:
                            result["default_obserr"] = err_val
                    except ValueError:
                        pass

    return result


class Digest2:
    """Stateful digest2 classifier. Loads model once, classifies many tracklets.

    Example::

        d2 = Digest2()
        results = d2.classify_file("observations.obs")
        for r in results:
            print(r.designation, r.noid.NEO)
        d2.close()

    Can also be used as a context manager::

        with Digest2() as d2:
            results = d2.classify_file("observations.obs")
    """

    # Class-level cache of (abbr, name) tuples
    _class_info = None

    def __init__(
        self,
        model_path: Optional[str] = None,
        config_path: Optional[str] = None,
        obscodes_path: Optional[str] = None,
        repeatable: bool = True,
        no_threshold: bool = False,
    ):
        """Initialize with model data.

        Args:
            model_path: Path to digest2.model.csv. Auto-discovered if None.
            config_path: Path to MPC.config for per-site errors. Auto-discovered if None.
            obscodes_path: Path to observatory codes file. Auto-discovered if None.
            repeatable: If True, use fixed random seed for deterministic results.
            no_threshold: If True, disable per-observation RMS ceiling clamping.
                When False (default), per-observation RMS values are clamped to
                at most 5x the configured observatory error. When True, only the
                floor (the configured error itself) is applied.
                Overrides any noThreshold setting in the config file.
        """
        if model_path is None:
            model_path = find_model_path()
        if obscodes_path is None:
            obscodes_path = find_obscodes_path()

        _extension.init(model_path, obscodes_path)
        _extension.configure(repeatable=1 if repeatable else 0)

        # Apply config file settings
        if config_path is None:
            config_path = find_config_path()

        if config_path is not None:
            cfg = _parse_config_file(config_path)
            kwargs = {}
            if cfg["default_obserr"] is not None:
                kwargs["obserr"] = cfg["default_obserr"]
            if cfg["repeatable"] is not None:
                kwargs["repeatable"] = 1 if cfg["repeatable"] else 0
            if cfg["no_threshold"] is not None:
                kwargs["no_threshold"] = 1 if cfg["no_threshold"] else 0
            if cfg["site_errors"]:
                kwargs["site_errors"] = cfg["site_errors"]
            if kwargs:
                _extension.configure(**kwargs)

        # Explicit no_threshold kwarg overrides config file
        _extension.configure(no_threshold=1 if no_threshold else 0)

        # Cache class info
        if Digest2._class_info is None:
            Digest2._class_info = _extension.get_classes()

        self._closed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """Release C resources."""
        if not self._closed:
            _extension.cleanup()
            self._closed = True

    def _check_open(self):
        if self._closed:
            raise RuntimeError("Digest2 instance has been closed")

    def classify_tracklet(
        self,
        observations: List[Observation],
        classes: Optional[List[str]] = None,
        is_ades: bool = False,
    ) -> ClassificationResult:
        """Classify a single tracklet.

        Args:
            observations: List of Observation objects (at least 2).
            classes: List of class abbreviations to compute (default: all).
                     e.g., ["NEO", "MC", "MB1"]
            is_ades: Whether these observations come from ADES format
                     (affects RMS computation).

        Returns:
            ClassificationResult with raw/noid Scores, rms, and rms_prime.
        """
        return self._score(observations, classes=classes, is_ades=is_ades)

    def _score(
        self,
        observations: List[Observation],
        classes: Optional[List[str]] = None,
        is_ades: bool = False,
        designation: str = "",
    ) -> ClassificationResult:
        """Internal: score a tracklet with an optional designation."""
        self._check_open()

        # Convert class abbreviations to indices
        class_indices = None
        if classes is not None:
            abbr_to_idx = {info[0]: i for i, info in enumerate(self._class_info)}
            class_indices = []
            for c in classes:
                if c not in abbr_to_idx:
                    raise ValueError(f"Unknown class abbreviation: {c}")
                class_indices.append(abbr_to_idx[c])

        # Convert observations to tuples for C extension
        obs_tuples = []
        for obs in observations:
            site_idx = _extension.parse_obscode(obs.obscode)
            obs_tuples.append(obs.to_tuple(site_idx))

        raw_result = _extension.score(
            obs_tuples,
            class_indices,
            1 if is_ades else 0,
        )

        return self._format_result(raw_result, designation=designation)

    def classify_file(
        self,
        filepath: str,
        classes: Optional[List[str]] = None,
    ) -> List[ClassificationResult]:
        """Classify all tracklets in an observation file.

        Supports MPC 80-column (.obs) and ADES XML (.xml) formats.

        Args:
            filepath: Path to the observation file.
            classes: List of class abbreviations to compute (default: all).

        Returns:
            List of ClassificationResult objects, one per tracklet.
        """
        self._check_open()

        is_xml = filepath.lower().endswith(".xml")

        if is_xml:
            tracklets = parse_ades_xml(filepath)
        else:
            tracklets = parse_mpc80_file(filepath)

        results = []
        for desig, obs_list in tracklets.items():
            if len(obs_list) < 2:
                continue

            try:
                result = self._score(
                    obs_list, classes=classes, is_ades=is_xml,
                    designation=desig.strip(),
                )
                results.append(result)
            except RuntimeError:
                # Skip tracklets that can't be scored (no motion, etc.)
                continue

        return results

    def classify_batch(
        self,
        tracklets: List[List[Observation]],
        classes: Optional[List[str]] = None,
    ) -> List[Optional[ClassificationResult]]:
        """Classify multiple tracklets.

        Args:
            tracklets: List of tracklets, each a list of Observations.
            classes: List of class abbreviations to compute.

        Returns:
            List of ClassificationResult objects (None for failed tracklets).
        """
        results = []
        for obs_list in tracklets:
            try:
                result = self.classify_tracklet(obs_list, classes=classes)
                results.append(result)
            except RuntimeError:
                results.append(None)
        return results

    def _format_result(
        self, raw_result: dict, designation: str = "",
    ) -> ClassificationResult:
        """Format raw C extension result into a ClassificationResult."""
        raw_scores = raw_result["raw_scores"]
        noid_scores = raw_result["noid_scores"]

        raw_kwargs = {}
        noid_kwargs = {}

        for i, (abbr, name) in enumerate(self._class_info):
            raw_kwargs[abbr] = raw_scores[i]
            noid_kwargs[abbr] = noid_scores[i]

        return ClassificationResult(
            raw=Scores(**raw_kwargs),
            noid=Scores(**noid_kwargs),
            rms=raw_result["rms"],
            rms_prime=raw_result["rms_prime"],
            designation=designation,
        )


def classify(
    input: Union[str, Path, List[Observation], List[List[Observation]]],
    model_path: Optional[str] = None,
    config_path: Optional[str] = None,
    obscodes_path: Optional[str] = None,
    classes: Optional[List[str]] = None,
    repeatable: bool = True,
    no_threshold: bool = False,
) -> Union[ClassificationResult, List[ClassificationResult]]:
    """One-shot classification. Accepts a filepath, tracklet, or batch.

    Args:
        input: One of:
            - A filepath (str or Path) to an observation file (.obs or .xml)
            - A list of Observation objects (single tracklet)
            - A list of lists of Observation objects (batch of tracklets)
        model_path: Path to model CSV (auto-discovered if None).
        config_path: Path to config file (auto-discovered if None).
        obscodes_path: Path to obscodes file (auto-discovered if None).
        classes: List of class abbreviations to compute.
        repeatable: Use fixed random seed for deterministic results.
        no_threshold: If True, disable per-observation RMS ceiling clamping.

    Returns:
        ClassificationResult for a single tracklet, or list of
        ClassificationResult for a file or batch.
    """
    with Digest2(
        model_path=model_path,
        config_path=config_path,
        obscodes_path=obscodes_path,
        repeatable=repeatable,
        no_threshold=no_threshold,
    ) as d2:
        if isinstance(input, (str, Path)):
            return d2.classify_file(str(input), classes=classes)
        if isinstance(input, list) and input and isinstance(input[0], list):
            return d2.classify_batch(input, classes=classes)
        return d2.classify_tracklet(input, classes=classes)
