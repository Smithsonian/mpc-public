"""Tests for the low-level C extension module (digest2._extension)."""

import math

import pytest

import digest2._extension as ext


class TestExtensionBasic:
    """Test basic extension functions that don't need initialization."""

    def test_get_classes(self):
        classes = ext.get_classes()
        assert len(classes) == 15
        assert classes[0] == ("Int", "MPC interest.")
        assert classes[1] == ("NEO", "NEO(q < 1.3)")

    def test_parse_obscode_valid(self):
        assert ext.parse_obscode("G96") == 1696
        assert ext.parse_obscode("500") == 500
        assert ext.parse_obscode("F51") == 1551

    def test_parse_obscode_invalid(self):
        with pytest.raises(ValueError):
            ext.parse_obscode("!!!")

    def test_is_initialized_before_init(self):
        assert ext.is_initialized() is False


class TestExtensionScoring:
    """Test scoring via the C extension."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, model_path, obscodes_path):
        ext.init(model_path, obscodes_path)
        ext.configure(repeatable=1)
        yield
        ext.cleanup()

    def test_is_initialized(self):
        assert ext.is_initialized() is True

    def test_score_sample_obs(self):
        """Test scoring the K16S99K sample tracklet.

        Expected results (matching CLI with repeatable, no config):
        NoID: Int=2, NEO=2, N22=1, N18=0, MC=2, MB1=85, MB2=3
        """
        g96 = ext.parse_obscode("G96")

        def date_to_mjd(year, month, day):
            flookup = [0, 306, 337, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275]
            z = year + int((month - 14) / 12)
            m = flookup[month] + 365 * z + z // 4 - z // 100 + z // 400 - 678882
            return m + day

        # K16S99K observations from sample.obs
        # Band G -> correction +0.24 to V
        obs = [
            (date_to_mjd(2022, 12, 25.384965),
             (8 * 3600 + 32 * 60 + 36.283) * math.pi / (12 * 3600),
             (17 * 3600 + 10 * 60 + 35.94) * math.pi / (180 * 3600),
             22.22, g96, 0.0, 0.0),
            (date_to_mjd(2022, 12, 25.395273),
             (8 * 3600 + 32 * 60 + 35.635) * math.pi / (12 * 3600),
             (17 * 3600 + 10 * 60 + 37.27) * math.pi / (180 * 3600),
             21.96, g96, 0.0, 0.0),
            (date_to_mjd(2022, 12, 25.400402),
             (8 * 3600 + 32 * 60 + 35.473) * math.pi / (12 * 3600),
             (17 * 3600 + 10 * 60 + 37.38) * math.pi / (180 * 3600),
             21.55, g96, 0.0, 0.0),
        ]

        result = ext.score(obs)

        assert "raw_scores" in result
        assert "noid_scores" in result
        assert "rms" in result
        assert "rms_prime" in result

        noid = result["noid_scores"]
        assert len(noid) == 15

        # MB1 (index 7) should be the dominant class
        assert noid[7] > 50  # MB1 = Inner Main Belt

        # RMS should be around 0.73
        assert abs(result["rms"] - 0.73) < 0.1

    def test_score_with_class_filter(self):
        """Test scoring with specific class indices."""
        g96 = ext.parse_obscode("G96")

        def date_to_mjd(year, month, day):
            flookup = [0, 306, 337, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275]
            z = year + int((month - 14) / 12)
            m = flookup[month] + 365 * z + z // 4 - z // 100 + z // 400 - 678882
            return m + day

        obs = [
            (date_to_mjd(2022, 12, 25.384965),
             (8 * 3600 + 32 * 60 + 36.283) * math.pi / (12 * 3600),
             (17 * 3600 + 10 * 60 + 35.94) * math.pi / (180 * 3600),
             22.22, g96, 0.0, 0.0),
            (date_to_mjd(2022, 12, 25.395273),
             (8 * 3600 + 32 * 60 + 35.635) * math.pi / (12 * 3600),
             (17 * 3600 + 10 * 60 + 37.27) * math.pi / (180 * 3600),
             21.96, g96, 0.0, 0.0),
        ]

        # Only compute NEO (index 1) and MB1 (index 7)
        result = ext.score(obs, [1, 7])
        assert result["noid_scores"][1] >= 0  # NEO
        assert result["noid_scores"][7] >= 0  # MB1

    def test_score_too_few_obs(self):
        """Test that scoring fails with fewer than 2 observations."""
        g96 = ext.parse_obscode("G96")
        obs = [(59938.0, 2.0, 0.3, 21.0, g96, 0.0, 0.0)]
        with pytest.raises(ValueError, match="At least 2"):
            ext.score(obs)

    def test_score_dict_format(self):
        """Test scoring with dict-format observations."""
        obs = [
            {"mjd": 59938.384965, "ra": 2.236660, "dec": 0.299789,
             "vmag": 22.22, "site": 1696},
            {"mjd": 59938.395273, "ra": 2.236613, "dec": 0.299796,
             "vmag": 21.96, "site": 1696},
        ]
        result = ext.score(obs)
        assert result["rms"] >= 0

    def test_configure_obserr(self):
        """Test setting default observatory error."""
        ext.configure(obserr=0.5)
        # Just check it doesn't crash

    def test_configure_site_errors(self):
        """Test setting per-site observatory errors."""
        ext.configure(site_errors={"G96": 0.29, "F51": 0.13})

    def test_configure_repeatable(self):
        """Test toggling repeatable mode."""
        ext.configure(repeatable=0)
        ext.configure(repeatable=1)


class TestExtensionInit:
    """Test initialization error handling."""

    def test_init_bad_model_path(self, obscodes_path):
        with pytest.raises(RuntimeError, match="model"):
            ext.init("/nonexistent/model.csv", obscodes_path)

    def test_init_bad_obscodes_path(self, model_path):
        with pytest.raises(RuntimeError, match="observatory"):
            ext.init(model_path, "/nonexistent/obscodes")

    def test_score_without_init(self):
        """Test that scoring without init gives an error."""
        # Make sure we're not initialized
        ext.cleanup()
        with pytest.raises(RuntimeError, match="not initialized"):
            ext.score([
                (59938.0, 2.0, 0.3, 21.0, 500, 0.0, 0.0),
                (59938.1, 2.1, 0.3, 21.0, 500, 0.0, 0.0),
            ])
