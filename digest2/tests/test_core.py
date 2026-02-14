"""Tests for the high-level Python API (digest2.core)."""

import tempfile
from pathlib import Path

import pytest

from digest2 import Digest2, classify, ClassificationResult, Scores
from digest2.observation import Observation, parse_mpc80_file


class TestDigest2Class:
    """Test the Digest2 stateful classifier."""

    def test_init_and_close(self, model_path, obscodes_path, empty_config_path):
        d2 = Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
        )
        d2.close()

    def test_context_manager(self, model_path, obscodes_path, empty_config_path):
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
        ) as d2:
            assert d2._closed is False
        assert d2._closed is True

    def test_classify_tracklet(self, model_path, obscodes_path, empty_config_path):
        obs = [
            Observation(mjd=59938.384965, ra=128.15118, dec=17.17665,
                        mag=22.22, band="G", obscode="G96"),
            Observation(mjd=59938.395273, ra=128.14899, dec=17.17702,
                        mag=21.96, band="G", obscode="G96"),
            Observation(mjd=59938.400402, ra=128.14780, dec=17.17717,
                        mag=21.55, band="G", obscode="G96"),
        ]

        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(obs)

        assert isinstance(result, ClassificationResult)
        assert isinstance(result.raw, Scores)
        assert isinstance(result.noid, Scores)
        assert result.rms >= 0
        assert result.rms_prime >= 0

        # MB1 should be dominant
        assert result.noid.MB1 > 50

    def test_classify_file(self, model_path, obscodes_path, sample_obs_path,
                           empty_config_path):
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            results = d2.classify_file(sample_obs_path)

        assert len(results) == 1
        r = results[0]
        assert isinstance(r, ClassificationResult)
        assert "K16S99K" in r.designation
        assert abs(r.rms - 0.73) < 0.1
        # NoID scores should match CLI
        assert round(r.noid.Int) == 2
        assert round(r.noid.NEO) == 2
        assert round(r.noid.MB1) == 85

    def test_classify_file_matches_cli(self, model_path, obscodes_path,
                                       sample_obs_path, empty_config_path):
        """Verify Python API matches CLI output for sample.obs.

        CLI with 'repeatable' config shows:
        K16S99K  0.73  Int=2 NEO=2 N22=1 N18=0 MC=2 MB1=85 MB2=3
        """
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            results = d2.classify_file(sample_obs_path)

        r = results[0]

        # These should match the CLI exactly (all rounded)
        assert round(r.noid.Int) == 2
        assert round(r.noid.NEO) == 2
        assert round(r.noid.N22) == 1
        assert round(r.noid.N18) == 0
        assert round(r.noid.MC) == 2
        assert round(r.noid.MB1) == 85
        assert round(r.noid.MB2) == 3

    def test_classify_tracklet_with_class_filter(self, model_path, obscodes_path,
                                                  empty_config_path):
        obs = [
            Observation(mjd=59938.384965, ra=128.15118, dec=17.17665,
                        mag=22.22, obscode="G96"),
            Observation(mjd=59938.395273, ra=128.14899, dec=17.17702,
                        mag=21.96, obscode="G96"),
        ]

        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            result = d2.classify_tracklet(obs, classes=["NEO", "MB1"])

        # Should still return all classes but only filtered ones computed
        assert result.noid.NEO >= 0
        assert result.noid.MB1 >= 0

    def test_classify_batch(self, model_path, obscodes_path, empty_config_path):
        obs1 = [
            Observation(mjd=59938.384965, ra=128.15118, dec=17.17665,
                        mag=22.22, obscode="G96"),
            Observation(mjd=59938.395273, ra=128.14899, dec=17.17702,
                        mag=21.96, obscode="G96"),
        ]
        obs2 = [
            Observation(mjd=59938.384965, ra=130.0, dec=20.0,
                        mag=20.0, obscode="G96"),
            Observation(mjd=59938.395273, ra=130.01, dec=20.01,
                        mag=20.0, obscode="G96"),
        ]

        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        ) as d2:
            results = d2.classify_batch([obs1, obs2])

        assert len(results) == 2
        assert results[0] is not None
        assert results[1] is not None
        assert isinstance(results[0], ClassificationResult)

    def test_closed_raises(self, model_path, obscodes_path, empty_config_path):
        d2 = Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
        )
        d2.close()
        with pytest.raises(RuntimeError, match="closed"):
            d2.classify_tracklet([
                Observation(mjd=59938.0, ra=128.0, dec=17.0, obscode="G96"),
                Observation(mjd=59938.1, ra=128.1, dec=17.1, obscode="G96"),
            ])

    def test_invalid_class_abbr(self, model_path, obscodes_path,
                                 empty_config_path):
        obs = [
            Observation(mjd=59938.0, ra=128.0, dec=17.0, obscode="G96"),
            Observation(mjd=59938.1, ra=128.1, dec=17.1, obscode="G96"),
        ]
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
        ) as d2:
            with pytest.raises(ValueError, match="Unknown class"):
                d2.classify_tracklet(obs, classes=["BOGUS"])

    def test_with_mpc_config(self, model_path, obscodes_path, mpc_config_path):
        """Test that applying MPC.config changes scores (G96 has 0.29 arcsec error)."""
        with Digest2(
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=mpc_config_path,
            repeatable=True,
        ) as d2:
            obs = [
                Observation(mjd=59938.384965, ra=128.15118, dec=17.17665,
                            mag=22.22, obscode="G96"),
                Observation(mjd=59938.395273, ra=128.14899, dec=17.17702,
                            mag=21.96, obscode="G96"),
                Observation(mjd=59938.400402, ra=128.14780, dec=17.17717,
                            mag=21.55, obscode="G96"),
            ]
            result = d2.classify_tracklet(obs)

        # With G96 error at 0.29 arcsec (vs default 1.0), scores change significantly.
        # With real site errors, this object scores as high-probability NEO.
        assert result.noid.NEO > 50


class TestClassifyFunction:
    """Test the polymorphic classify() convenience function."""

    def test_classify_single_tracklet(self, model_path, obscodes_path,
                                       empty_config_path):
        obs = [
            Observation(mjd=59938.384965, ra=128.15118, dec=17.17665,
                        mag=22.22, obscode="G96"),
            Observation(mjd=59938.395273, ra=128.14899, dec=17.17702,
                        mag=21.96, obscode="G96"),
        ]

        result = classify(
            obs,
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        )

        assert isinstance(result, ClassificationResult)
        assert isinstance(result.raw, Scores)
        assert isinstance(result.noid, Scores)
        assert result.rms >= 0

    def test_classify_filepath_str(self, model_path, obscodes_path,
                                    sample_obs_path, empty_config_path):
        results = classify(
            sample_obs_path,
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        )

        assert isinstance(results, list)
        assert len(results) == 1
        assert "K16S99K" in results[0].designation

    def test_classify_filepath_path(self, model_path, obscodes_path,
                                     sample_obs_path, empty_config_path):
        results = classify(
            Path(sample_obs_path),
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        )

        assert isinstance(results, list)
        assert len(results) == 1
        assert "K16S99K" in results[0].designation

    def test_classify_batch(self, model_path, obscodes_path, empty_config_path):
        obs1 = [
            Observation(mjd=59938.384965, ra=128.15118, dec=17.17665,
                        mag=22.22, obscode="G96"),
            Observation(mjd=59938.395273, ra=128.14899, dec=17.17702,
                        mag=21.96, obscode="G96"),
        ]
        obs2 = [
            Observation(mjd=59938.384965, ra=130.0, dec=20.0,
                        mag=20.0, obscode="G96"),
            Observation(mjd=59938.395273, ra=130.01, dec=20.01,
                        mag=20.0, obscode="G96"),
        ]

        results = classify(
            [obs1, obs2],
            model_path=model_path,
            obscodes_path=obscodes_path,
            config_path=empty_config_path,
            repeatable=True,
        )

        assert isinstance(results, list)
        assert len(results) == 2
        assert results[0] is not None
        assert results[1] is not None


class TestScoresDataclass:
    """Test the Scores dataclass convenience methods."""

    def test_getitem(self):
        s = Scores(NEO=42.5, MB1=57.5)
        assert s["NEO"] == 42.5
        assert s["MB1"] == 57.5
        assert s["Int"] == 0.0

    def test_getitem_invalid_key(self):
        s = Scores()
        with pytest.raises(KeyError):
            s["BOGUS"]

    def test_items(self):
        s = Scores(NEO=10.0, MB1=90.0)
        items = dict(s.items())
        assert items["NEO"] == 10.0
        assert items["MB1"] == 90.0
        assert items["Int"] == 0.0
        assert len(items) == 15

    def test_iter(self):
        s = Scores()
        abbrs = list(s)
        assert abbrs == [
            "Int", "NEO", "N22", "N18", "MC", "Hun", "Pho",
            "MB1", "Pal", "Han", "MB2", "MB3", "Hil", "JTr", "JFC",
        ]

    def test_frozen(self):
        s = Scores(NEO=42.5)
        with pytest.raises(AttributeError):
            s.NEO = 99.0


class TestClassificationResult:
    """Test the ClassificationResult dataclass."""

    def test_top_class(self):
        noid = Scores(NEO=10.0, MB1=80.0, MC=5.0)
        result = ClassificationResult(
            raw=Scores(), noid=noid, rms=0.5, rms_prime=0.0,
        )
        assert result.top_class == "MB1"

    def test_top_class_neo(self):
        noid = Scores(NEO=90.0, MB1=5.0)
        result = ClassificationResult(
            raw=Scores(), noid=noid, rms=0.5, rms_prime=0.0,
        )
        assert result.top_class == "NEO"

    def test_designation_default(self):
        result = ClassificationResult(
            raw=Scores(), noid=Scores(), rms=0.0, rms_prime=0.0,
        )
        assert result.designation == ""

    def test_frozen(self):
        result = ClassificationResult(
            raw=Scores(), noid=Scores(), rms=0.0, rms_prime=0.0,
        )
        with pytest.raises(AttributeError):
            result.rms = 99.0
