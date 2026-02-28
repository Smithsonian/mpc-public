"""Tests for observation parsing (digest2.observation)."""

import math
import tempfile
from pathlib import Path

import pytest

from digest2.observation import (
    Observation,
    _date_to_mjd,
    _update_magnitude,
    parse_mpc80,
    parse_mpc80_file,
)


class TestDateToMjd:
    """Test MJD conversion."""

    def test_known_date(self):
        """Test a known date: 2000 Jan 1.5 = MJD 51544.5 (J2000.0)."""
        mjd = _date_to_mjd(2000, 1, 1.5)
        assert abs(mjd - 51544.5) < 0.001

    def test_december_date(self):
        """Test December date (exercises C-style integer division)."""
        # 2022 Dec 25.0
        mjd = _date_to_mjd(2022, 12, 25.0)
        # Expected: MJD 59938.0 (approximately)
        assert abs(mjd - 59938.0) < 1.0

    def test_matches_c_code(self):
        """Test that MJD calculation matches C code exactly.

        C code: z = year + (month - 14) / 12 uses truncation toward zero.
        For month=12: (12-14)/12 = -2/12 = 0 in C, -1 in Python floor division.
        """
        # Verify C-style division is used
        mjd = _date_to_mjd(2022, 12, 25.384965)
        assert abs(mjd - 59938.384965) < 0.001


class TestUpdateMagnitude:
    """Test band correction."""

    def test_v_band_no_correction(self):
        assert _update_magnitude("V", 21.0) == 21.0

    def test_g_band_correction(self):
        assert abs(_update_magnitude("G", 21.0) - 21.24) < 0.001

    def test_r_band_correction(self):
        assert abs(_update_magnitude("r", 21.0) - 21.23) < 0.001

    def test_zero_mag_no_correction(self):
        assert _update_magnitude("B", 0.0) == 0.0

    def test_unknown_band(self):
        # Default correction is -0.8
        assert abs(_update_magnitude("X", 21.0) - 20.2) < 0.001


class TestObservation:
    """Test Observation dataclass."""

    def test_create(self):
        obs = Observation(mjd=59938.0, ra=128.15, dec=17.18)
        assert obs.mjd == 59938.0
        assert obs.mag == 0.0
        assert obs.obscode == "500"

    def test_ra_rad(self):
        obs = Observation(mjd=59938.0, ra=180.0, dec=0.0)
        assert abs(obs.ra_rad - math.pi) < 1e-10

    def test_dec_rad(self):
        obs = Observation(mjd=59938.0, ra=0.0, dec=90.0)
        assert abs(obs.dec_rad - math.pi / 2) < 1e-10

    def test_to_tuple(self):
        obs = Observation(mjd=59938.0, ra=128.15, dec=17.18, mag=21.5,
                          obscode="G96", rms_ra=0.5, rms_dec=0.3)
        t = obs.to_tuple(site_index=1696)
        assert t[0] == 59938.0  # mjd
        assert abs(t[1] - math.radians(128.15)) < 1e-10  # ra_rad
        assert abs(t[2] - math.radians(17.18)) < 1e-10  # dec_rad
        assert t[3] == 21.5  # vmag
        assert t[4] == 1696  # site
        assert t[5] == 0.5  # rmsRA
        assert t[6] == 0.3  # rmsDec
        assert t[7] == 0  # spacebased


class TestParseMpc80:
    """Test MPC 80-column line parsing."""

    def test_parse_sample_line(self):
        line = "     K16S99K 1C2022 12 25.38496508 32 36.283+17 10 35.94         21.98GV     G96"
        obs = parse_mpc80(line)
        assert obs is not None
        assert abs(obs.mjd - 59938.384965) < 0.001
        assert abs(obs.ra - 128.15118) < 0.001
        assert abs(obs.dec - 17.17665) < 0.001
        assert obs.band == "G"
        assert obs.obscode == "G96"
        # Magnitude corrected from G band: 21.98 + 0.24 = 22.22
        assert abs(obs.mag - 22.22) < 0.01

    def test_parse_short_line(self):
        obs = parse_mpc80("too short")
        assert obs is None

    def test_parse_non_optical(self):
        # Note2 field (col 14) must be C, S, or B
        line = "     K16S99K 1X2022 12 25.38496508 32 36.283+17 10 35.94         21.98GV     G96"
        obs = parse_mpc80(line)
        assert obs is None

    def test_parse_negative_declination(self):
        line = "     K16S99K 1C2022 12 25.38496508 32 36.283-17 10 35.94         21.98GV     G96"
        obs = parse_mpc80(line)
        assert obs is not None
        assert obs.dec < 0


class TestParseMpc80File:
    """Test MPC 80-column file parsing."""

    def test_parse_sample_file(self, sample_obs_path):
        tracklets = parse_mpc80_file(sample_obs_path)
        assert len(tracklets) == 1

        # Get the single tracklet
        desig = list(tracklets.keys())[0]
        assert "K16S99K" in desig

        obs_list = tracklets[desig]
        assert len(obs_list) == 3

    def test_parse_empty_file(self, tmp_path):
        f = tmp_path / "empty.obs"
        f.write_text("")
        tracklets = parse_mpc80_file(str(f))
        assert len(tracklets) == 0

    def test_parse_multiple_objects(self, tmp_path):
        content = (
            "     K16S99K 1C2022 12 25.38496508 32 36.283+17 10 35.94         21.98GV     G96\n"
            "     K16S99K 1C2022 12 25.39527308 32 35.635+17 10 37.27         21.72GV     G96\n"
            "     K16S99L 1C2022 12 25.38496508 33 36.283+17 10 35.94         21.98GV     G96\n"
            "     K16S99L 1C2022 12 25.39527308 33 35.635+17 10 37.27         21.72GV     G96\n"
        )
        f = tmp_path / "multi.obs"
        f.write_text(content)
        tracklets = parse_mpc80_file(str(f))
        assert len(tracklets) == 2
