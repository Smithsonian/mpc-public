"""Tests for the trial orbit collection feature (collect_orbits=True).

Tests cover:
- Basic orbit collection via classify_tracklet
- Default behavior (no orbits when collect_orbits=False)
- Score consistency between score() and score_orbits()
- Trial orbit field validity (ranges, types)
- orbit_elements numpy array conversion
- All API entry points (classify_file, classify_batch, classify convenience)
- Class filter interaction with orbit collection
- Low-level _extension.score_orbits() function
"""
import math

import pytest
import numpy as np

from digest2 import Digest2, classify, ClassificationResult, TrialOrbit
from digest2.observation import Observation
import digest2._extension as ext


# --- Helper ---

def _make_sample_obs():
    """Return 3 Observation objects for K16S99K (2016 SK99) from G96."""
    return [
        Observation(
            mjd=59938.384965, ra=128.15118, dec=17.17665,
            mag=21.98, band="G", obscode="G96",
        ),
        Observation(
            mjd=59938.395273, ra=128.15652, dec=17.17702,
            mag=21.72, band="G", obscode="G96",
        ),
        Observation(
            mjd=59938.400402, ra=128.14789, dec=17.17705,
            mag=21.31, band="G", obscode="G96",
        ),
    ]


def _make_extension_obs():
    """Return observation tuples suitable for ext.score() / ext.score_orbits()."""
    g96 = ext.parse_obscode("G96")
    return [
        (
            59938.384965,
            (8 * 3600 + 32 * 60 + 36.283) * math.pi / (12 * 3600),
            (17 * 3600 + 10 * 60 + 35.94) * math.pi / (180 * 3600),
            22.22,
            g96,
            0.0,
            0.0,
        ),
        (
            59938.395273,
            (8 * 3600 + 32 * 60 + 35.635) * math.pi / (12 * 3600),
            (17 * 3600 + 10 * 60 + 37.27) * math.pi / (180 * 3600),
            21.72,
            g96,
            0.0,
            0.0,
        ),
        (
            59938.400402,
            (8 * 3600 + 32 * 60 + 35.473) * math.pi / (12 * 3600),
            (17 * 3600 + 10 * 60 + 37.38) * math.pi / (180 * 3600),
            21.31,
            g96,
            0.0,
            0.0,
        ),
    ]


# --- Tests: Basic collection ---


class TestTrialOrbitBasic:
    """Basic tests for collect_orbits=True."""

    def test_collect_orbits_basic(
        self, model_path, obscodes_path, empty_config_path
    ):
        """classify_tracklet with collect_orbits=True returns trial orbits."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(obs, collect_orbits=True)

        assert isinstance(result, ClassificationResult)
        assert result.trial_orbits is not None
        assert len(result.trial_orbits) > 0
        # Spot-check first few are TrialOrbit instances
        assert all(isinstance(t, TrialOrbit) for t in result.trial_orbits[:10])

    def test_default_no_orbits(
        self, model_path, obscodes_path, empty_config_path
    ):
        """Without collect_orbits, trial_orbits is None."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(obs)

        assert result.trial_orbits is None
        assert result.orbit_elements is None

    def test_score_consistency(
        self, model_path, obscodes_path, empty_config_path
    ):
        """score() and score_orbits() produce identical scores."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            r_without = d2.classify_tracklet(obs, collect_orbits=False)
            r_with = d2.classify_tracklet(obs, collect_orbits=True)

        # Compare all 15 raw and noid scores
        for abbr, val_without in r_without.raw.items():
            assert val_without == pytest.approx(r_with.raw[abbr], abs=1e-10), (
                f"raw {abbr} mismatch"
            )
        for abbr, val_without in r_without.noid.items():
            assert val_without == pytest.approx(r_with.noid[abbr], abs=1e-10), (
                f"noid {abbr} mismatch"
            )
        assert r_without.rms == pytest.approx(r_with.rms, abs=1e-10)


# --- Tests: Field validity ---


class TestTrialOrbitValidity:
    """Tests that trial orbit field values are within expected ranges."""

    def test_trial_orbit_field_validity(
        self, model_path, obscodes_path, empty_config_path
    ):
        """All trial orbits have physically valid field values."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(obs, collect_orbits=True)

        # Check first 1000 orbits (representative sample)
        for t in result.trial_orbits[:1000]:
            assert t.q > 0, f"q must be positive, got {t.q}"
            assert t.e >= 0, f"e must be non-negative, got {t.e}"
            assert 0 <= t.i <= 180, f"i must be 0-180 deg, got {t.i}"
            assert 0 <= t.iq <= 28, f"iq out of range: {t.iq}"
            assert 0 <= t.ie <= 7, f"ie out of range: {t.ie}"
            assert 0 <= t.ii <= 10, f"ii out of range: {t.ii}"
            assert 0 <= t.ih <= 17, f"ih out of range: {t.ih}"
            assert isinstance(t.new_tag, bool)
            assert t.d > 0, f"geocentric distance must be positive"
            assert 0 < t.an < math.pi, f"angle out of range: {t.an}"


# --- Tests: orbit_elements property ---


class TestOrbitElements:
    """Tests for the orbit_elements property (numpy array conversion)."""

    def test_orbit_elements_property(
        self, model_path, obscodes_path, empty_config_path
    ):
        """orbit_elements returns dict of numpy arrays with correct shapes/dtypes."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(obs, collect_orbits=True)

        elems = result.orbit_elements
        assert elems is not None
        expected_keys = {"q", "e", "i", "H", "d", "an", "iq", "ie", "ii", "ih", "new_tag"}
        assert set(elems.keys()) == expected_keys

        n = len(result.trial_orbits)
        for key in ["q", "e", "i", "H", "d", "an"]:
            assert elems[key].shape == (n,), f"{key} shape mismatch"
            assert elems[key].dtype == np.float64, f"{key} dtype mismatch"
        for key in ["iq", "ie", "ii", "ih"]:
            assert elems[key].shape == (n,), f"{key} shape mismatch"
            assert elems[key].dtype == np.int32, f"{key} dtype mismatch"
        assert elems["new_tag"].shape == (n,)
        assert elems["new_tag"].dtype == np.bool_

        # Repeated access should reuse the cached arrays.
        elems2 = result.orbit_elements
        assert elems2 is elems

    def test_orbit_elements_none_when_no_orbits(
        self, model_path, obscodes_path, empty_config_path
    ):
        """When trial_orbits is None, orbit_elements returns None."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(obs, collect_orbits=False)
        assert result.orbit_elements is None


# --- Tests: All API entry points ---


class TestCollectOrbitsAPIMethods:
    """Tests that collect_orbits works through all API entry points."""

    def test_classify_file(
        self, model_path, obscodes_path, empty_config_path, sample_obs_path
    ):
        """classify_file with collect_orbits=True returns trial orbits."""
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            results = d2.classify_file(sample_obs_path, collect_orbits=True)
        assert len(results) >= 1
        assert results[0].trial_orbits is not None
        assert len(results[0].trial_orbits) > 0

    def test_classify_batch(
        self, model_path, obscodes_path, empty_config_path
    ):
        """classify_batch with collect_orbits=True returns trial orbits."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            results = d2.classify_batch([obs], collect_orbits=True)
        assert len(results) == 1
        assert results[0] is not None
        assert results[0].trial_orbits is not None

    def test_classify_convenience(
        self, model_path, obscodes_path, empty_config_path, sample_obs_path
    ):
        """classify() convenience function with collect_orbits=True."""
        results = classify(
            sample_obs_path,
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
            collect_orbits=True,
        )
        assert len(results) >= 1
        assert results[0].trial_orbits is not None

    def test_collect_with_class_filter(
        self, model_path, obscodes_path, empty_config_path
    ):
        """collect_orbits=True works with class filter."""
        obs = _make_sample_obs()
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(
                obs, classes=["NEO", "MB1"], collect_orbits=True
            )
        assert result.trial_orbits is not None
        assert len(result.trial_orbits) > 0


# --- Tests: Low-level extension ---


class TestExtensionScoreOrbits:
    """Low-level tests for _extension.score_orbits()."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, model_path, obscodes_path):
        ext.init(model_path, obscodes_path)
        ext.configure(repeatable=1)
        yield
        ext.cleanup()

    def test_score_orbits_basic(self):
        """score_orbits returns dict with trial_orbits key and valid data."""
        obs = _make_extension_obs()
        result = ext.score_orbits(obs)

        assert "trial_orbits" in result
        assert "n_orbits" in result
        assert result["n_orbits"] > 0
        assert len(result["trial_orbits"]) == result["n_orbits"]

        # Each orbit is an 11-element tuple
        orb = result["trial_orbits"][0]
        assert len(orb) == 11
        assert isinstance(orb[0], float)  # q
        assert isinstance(orb[1], float)  # e
        assert isinstance(orb[6], int)  # iq

        # Scores should also be present
        assert "raw_scores" in result
        assert "noid_scores" in result
        assert "rms" in result
        assert len(result["raw_scores"]) == 15
        assert len(result["noid_scores"]) == 15
