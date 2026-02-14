"""Tests for digest2.population — population model generation pipeline."""

import math
import tempfile
from pathlib import Path

import numpy as np
import pytest

from digest2.population import (
    CLASS_ABBR,
    CLASS_HEADING,
    CLASS_TESTS,
    D2CLASSES,
    EPART,
    EX,
    HPART,
    HX,
    IPART,
    IX,
    QPART,
    QX,
    build_model,
    h_to_bin,
    is_hansa,
    is_hilda,
    is_hungaria,
    is_inner_mb,
    is_jfc,
    is_mars_crosser,
    is_mid_mb,
    is_mpcint,
    is_neo,
    is_h18neo,
    is_h22neo,
    is_outer_mb,
    is_pallas,
    is_phocaea,
    is_trojan,
    qei_to_bin,
    qeih_to_bin,
    read_model_csv,
    read_s3m,
    write_model_csv,
    _volume_scale,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def s3m_path():
    """Return path to the existing s3m.dat file."""
    p = Path(__file__).parent.parent / "population" / "make_population" / "s3m.dat"
    if not p.exists():
        pytest.skip("s3m.dat not found")
    return str(p)


@pytest.fixture
def existing_model_path():
    """Return path to the existing digest2.model.csv."""
    p = Path(__file__).parent.parent / "population" / "digest2.model.csv"
    if not p.exists():
        pytest.skip("digest2.model.csv not found")
    return str(p)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_dimensions(self):
        assert QX == 29
        assert EX == 8
        assert IX == 11
        assert HX == 18
        assert D2CLASSES == 15

    def test_partition_lengths(self):
        assert len(QPART) == QX
        assert len(EPART) == EX
        assert len(IPART) == IX
        assert len(HPART) == HX

    def test_partition_sorted(self):
        assert all(QPART[i] < QPART[i + 1] for i in range(QX - 1))
        assert all(EPART[i] < EPART[i + 1] for i in range(EX - 1))
        assert all(IPART[i] < IPART[i + 1] for i in range(IX - 1))
        assert all(HPART[i] < HPART[i + 1] for i in range(HX - 1))

    def test_class_arrays(self):
        assert len(CLASS_ABBR) == D2CLASSES
        assert len(CLASS_HEADING) == D2CLASSES
        assert len(CLASS_TESTS) == D2CLASSES


# ---------------------------------------------------------------------------
# Binning
# ---------------------------------------------------------------------------

class TestBinning:
    def test_qeih_in_model(self):
        """A typical main-belt orbit should bin successfully."""
        result = qeih_to_bin(q=2.3, e=0.15, i=8.0, h=15.0)
        assert result is not None
        iq, ie, ii, ih = result
        assert 0 <= iq < QX
        assert 0 <= ie < EX
        assert 0 <= ii < IX
        assert 0 <= ih < HX

    def test_qeih_out_of_model_q(self):
        """q >= 100 is out of model."""
        assert qeih_to_bin(q=100.0, e=0.1, i=5.0, h=15.0) is None

    def test_qeih_out_of_model_e(self):
        """e >= 1.1 is out of model."""
        assert qeih_to_bin(q=1.0, e=1.1, i=5.0, h=15.0) is None

    def test_qeih_out_of_model_i(self):
        """i >= 180 is out of model."""
        assert qeih_to_bin(q=1.0, e=0.1, i=180.0, h=15.0) is None

    def test_h_to_bin_boundaries(self):
        """H values map to correct bins."""
        # H < 6 → bin 0
        assert h_to_bin(5.0) == 0
        # H = 6.0 → bin 1 (>= 6, < 8)
        assert h_to_bin(6.0) == 1
        # H = 7.9 → bin 1
        assert h_to_bin(7.9) == 1
        # H >= 25.5 → last bin (HX-1 = 17)
        assert h_to_bin(30.0) == HX - 1

    def test_qei_to_bin_first_bin(self):
        """Very small q, e, i should give (0, 0, 0)."""
        result = qei_to_bin(q=0.1, e=0.01, i=0.5)
        assert result == (0, 0, 0)

    def test_qeih_to_bin_known_orbit(self):
        """Test a known NEO orbit: q=0.5, e=0.6, i=10, H=20."""
        result = qeih_to_bin(0.5, 0.6, 10.0, 20.0)
        assert result is not None
        iq, ie, ii, ih = result
        # q=0.5 is in bin 1 (between 0.4 and 0.7)
        assert iq == 1
        # e=0.6 is in bin 5 (between 0.5 and 0.7)
        assert ie == 5
        # i=10 is in bin 2 (between 5 and 10: i=10 >= 10, so bin 3)
        # Actually: i >= IPART[2]=10, so we go to bin 3
        assert ii == 3
        # H=20 is in bin 12 (between 19 and 20: h=20 >= 20, so bin 13)
        assert ih == 13


# ---------------------------------------------------------------------------
# Class test functions
# ---------------------------------------------------------------------------

class TestClassTests:
    def test_is_neo(self):
        assert is_neo(1.0, 0.3, 10, 20) is True
        assert is_neo(1.3, 0.3, 10, 20) is False

    def test_is_h22neo(self):
        assert is_h22neo(1.0, 0.3, 10, 20) is True
        assert is_h22neo(1.0, 0.3, 10, 23) is False
        assert is_h22neo(1.5, 0.3, 10, 20) is False

    def test_is_h18neo(self):
        assert is_h18neo(1.0, 0.3, 10, 17) is True
        assert is_h18neo(1.0, 0.3, 10, 19) is False

    def test_is_mpcint_neo(self):
        """NEO is always MPC interesting."""
        assert is_mpcint(1.0, 0.3, 10, 20) is True

    def test_is_mpcint_high_e(self):
        """High eccentricity is MPC interesting."""
        assert is_mpcint(2.0, 0.6, 10, 15) is True

    def test_is_mpcint_high_i(self):
        """High inclination is MPC interesting."""
        assert is_mpcint(2.5, 0.1, 45, 15) is True

    def test_is_mpcint_normal_mb(self):
        """Normal main belt is NOT MPC interesting."""
        assert is_mpcint(2.5, 0.1, 5, 15) is False

    def test_is_mars_crosser(self):
        # q=1.5, e=0.2 → a=1.875, Q = a*(1+e) = 2.25 > 1.58
        assert is_mars_crosser(1.5, 0.2, 10, 15) is True
        # q < 1.3 is NEO, not Mars Crosser
        assert is_mars_crosser(1.2, 0.2, 10, 15) is False

    def test_is_hungaria(self):
        # a=1.9, e=0.1 → q = 1.9*0.9 = 1.71, i=22
        assert is_hungaria(1.71, 0.1, 22, 15) is True
        assert is_hungaria(1.71, 0.3, 22, 15) is False  # e too high

    def test_is_phocaea(self):
        # a=2.3, e=0.2 → q = 2.3*0.8 = 1.84, i=23
        assert is_phocaea(1.84, 0.2, 23, 15) is True
        assert is_phocaea(1.84, 0.2, 30, 15) is False  # i too high

    def test_is_inner_mb(self):
        # a=2.3, e=0.1 → q = 2.3*0.9 = 2.07, i=5
        assert is_inner_mb(2.07, 0.1, 5, 15) is True
        assert is_inner_mb(1.5, 0.1, 5, 15) is False  # q too low

    def test_is_pallas(self):
        # a=2.7, e=0.2 → q = 2.7*0.8 = 2.16, i=30
        assert is_pallas(2.16, 0.2, 30, 15) is True
        assert is_pallas(2.16, 0.2, 10, 15) is False  # i too low

    def test_is_hansa(self):
        # a=2.6, e=0.1 → q = 2.6*0.9 = 2.34, i=22
        assert is_hansa(2.34, 0.1, 22, 15) is True
        assert is_hansa(2.34, 0.1, 25, 15) is False  # i too high

    def test_is_mid_mb(self):
        # a=2.6, e=0.1 → q = 2.6*0.9 = 2.34, i=10
        assert is_mid_mb(2.34, 0.1, 10, 15) is True
        assert is_mid_mb(2.34, 0.1, 25, 15) is False  # i too high

    def test_is_outer_mb(self):
        # a=3.0, e=0.1 → q = 3.0*0.9 = 2.7, i=15
        assert is_outer_mb(2.7, 0.1, 15, 15) is True
        assert is_outer_mb(2.7, 0.5, 15, 15) is False  # e too high

    def test_is_hilda(self):
        # a=3.96, e=0.1 → q = 3.96*0.9 = 3.564, i=10
        assert is_hilda(3.564, 0.1, 10, 15) is True
        assert is_hilda(3.564, 0.1, 20, 15) is False  # i too high

    def test_is_trojan(self):
        # a=5.2, e=0.1 → q = 5.2*0.9 = 4.68, i=15
        assert is_trojan(4.68, 0.1, 15, 15) is True
        assert is_trojan(4.68, 0.3, 15, 15) is False  # e too high

    def test_is_jfc(self):
        # Typical JFC: q=1.5, e=0.7, i=10
        # a = q/(1-e) = 5, Tj = 5.2*(0.3)/1.5 + 2*sqrt(1.5*1.7/5.2)*cos(10°)
        # = 1.04 + 2*0.7*0.985 ≈ 1.04 + 1.379 ≈ 2.42
        assert is_jfc(1.5, 0.7, 10, 15) is True
        # q < 1.3 → excluded
        assert is_jfc(1.0, 0.7, 10, 15) is False

    def test_class_count(self):
        """15 class test functions."""
        assert len(CLASS_TESTS) == 15


# ---------------------------------------------------------------------------
# Read existing s3m.dat
# ---------------------------------------------------------------------------

class TestReadS3m:
    def test_read_s3m_dimensions(self, s3m_path):
        all_ss, all_class = read_s3m(s3m_path)
        assert all_ss.shape == (QX, EX, IX, HX)
        assert all_class.shape == (D2CLASSES, QX, EX, IX, HX)

    def test_read_s3m_nonneg(self, s3m_path):
        all_ss, all_class = read_s3m(s3m_path)
        assert np.all(all_ss >= 0)
        assert np.all(all_class >= 0)

    def test_read_s3m_has_data(self, s3m_path):
        all_ss, all_class = read_s3m(s3m_path)
        assert all_ss.sum() > 0
        assert all_class.sum() > 0

    def test_read_s3m_class_leq_ss(self, s3m_path):
        """Each class count should not exceed the SS count in that bin."""
        all_ss, all_class = read_s3m(s3m_path)
        for c in range(D2CLASSES):
            assert np.all(all_class[c] <= all_ss + 1e-9)


# ---------------------------------------------------------------------------
# Read existing digest2.model.csv
# ---------------------------------------------------------------------------

class TestReadModelCSV:
    def test_read_existing_model_shape(self, existing_model_path):
        model = read_model_csv(existing_model_path)
        assert model["all_ss"].shape == (QX, EX, IX, HX)
        assert model["unk_ss"].shape == (QX, EX, IX, HX)
        assert model["all_class"].shape == (D2CLASSES, QX, EX, IX, HX)
        assert model["unk_class"].shape == (D2CLASSES, QX, EX, IX, HX)

    def test_read_existing_model_has_data(self, existing_model_path):
        model = read_model_csv(existing_model_path)
        assert model["all_ss"].sum() > 0
        assert model["unk_ss"].sum() > 0

    def test_read_existing_model_all_keys(self, existing_model_path):
        model = read_model_csv(existing_model_path)
        assert set(model.keys()) == {"all_ss", "unk_ss", "all_class", "unk_class"}


# ---------------------------------------------------------------------------
# Write / read round-trip
# ---------------------------------------------------------------------------

class TestWriteReadRoundTrip:
    def test_roundtrip(self, tmp_path):
        """Write model CSV then read it back, verify arrays match."""
        rng = np.random.default_rng(42)
        all_ss = rng.random((QX, EX, IX, HX)) * 100
        unk_ss = rng.random((QX, EX, IX, HX)) * 50
        all_class = rng.random((D2CLASSES, QX, EX, IX, HX)) * 80
        unk_class = rng.random((D2CLASSES, QX, EX, IX, HX)) * 30

        csv_path = str(tmp_path / "test_model.csv")
        write_model_csv(csv_path, all_ss, unk_ss, all_class, unk_class)

        result = read_model_csv(csv_path)
        np.testing.assert_allclose(result["all_ss"], all_ss, rtol=1e-12)
        np.testing.assert_allclose(result["unk_ss"], unk_ss, rtol=1e-12)
        np.testing.assert_allclose(result["all_class"], all_class, rtol=1e-12)
        np.testing.assert_allclose(result["unk_class"], unk_class, rtol=1e-12)

    def test_roundtrip_zeros(self, tmp_path):
        """Zero-valued bins should produce empty CSV fields."""
        all_ss = np.zeros((QX, EX, IX, HX))
        unk_ss = np.zeros((QX, EX, IX, HX))
        all_class = np.zeros((D2CLASSES, QX, EX, IX, HX))
        unk_class = np.zeros((D2CLASSES, QX, EX, IX, HX))

        # Set a few non-zero values
        all_ss[5, 2, 3, 10] = 42.0
        unk_ss[5, 2, 3, 10] = 17.0

        csv_path = str(tmp_path / "test_zeros.csv")
        write_model_csv(csv_path, all_ss, unk_ss, all_class, unk_class)
        result = read_model_csv(csv_path)

        np.testing.assert_array_equal(result["all_ss"], all_ss)
        np.testing.assert_array_equal(result["unk_ss"], unk_ss)


# ---------------------------------------------------------------------------
# Volume scaling
# ---------------------------------------------------------------------------

class TestVolumeScaling:
    def test_scaling_computation(self):
        """Verify scaling on a known single bin."""
        all_ss = np.zeros((QX, EX, IX, HX))
        known_ss = np.zeros((QX, EX, IX, HX))
        all_class = np.zeros((D2CLASSES, QX, EX, IX, HX))
        known_class = np.zeros((D2CLASSES, QX, EX, IX, HX))

        # Put data in a single bin: iq=0, ie=0, ii=0, ih=0
        all_ss[0, 0, 0, 0] = 100.0
        known_ss[0, 0, 0, 0] = 30.0

        unk_ss, unk_class = _volume_scale(
            all_ss, known_ss, all_class, known_class)

        # Compute expected isqv for bin (0,0,0,0):
        # dq = QPART[0] - 0 = 0.4
        # de = EPART[0] - 0 = 0.1,  d0=1.0, d1=1-0.1=0.9
        # dae = 0.4 * 0.1 / (1.0 + 0.9) = 0.04/1.9
        # di = IPART[0] - 0 = 2
        # daei = (0.04/1.9) * 2
        # dh = HPART[0] - 0 = 6
        # isqv = 1/sqrt(daei * 6)
        dq = 0.4
        dae = dq * 0.1 / (1.0 + 0.9)
        daei = dae * 2.0
        isqv = 1.0 / math.sqrt(daei * 6.0)

        np.testing.assert_allclose(all_ss[0, 0, 0, 0], 100.0 * isqv, rtol=1e-12)
        np.testing.assert_allclose(unk_ss[0, 0, 0, 0], 70.0 * isqv, rtol=1e-12)

    def test_scaling_unk_nonneg_when_known_leq_all(self):
        """When known <= all, unk should be non-negative."""
        rng = np.random.default_rng(123)
        all_ss = rng.random((QX, EX, IX, HX)) * 100
        known_ss = all_ss * rng.random((QX, EX, IX, HX))  # always <= all
        all_class = rng.random((D2CLASSES, QX, EX, IX, HX)) * 80
        known_class = all_class * rng.random((D2CLASSES, QX, EX, IX, HX))

        unk_ss, unk_class = _volume_scale(
            all_ss.copy(), known_ss.copy(),
            all_class.copy(), known_class.copy())

        assert np.all(unk_ss >= -1e-10)


# ---------------------------------------------------------------------------
# Build model from s3m.dat (integration test)
# ---------------------------------------------------------------------------

class TestBuildModelFromS3m:
    def test_build_with_mock_catalog(self, s3m_path, tmp_path):
        """Build a model from real s3m.dat and a tiny mock astorb catalog."""
        # Create a minimal mock astorb.dat line
        # Fields (0-indexed character positions):
        #   H:   42-46
        #   i:   147-156
        #   e:   158-167
        #   a:   169-180
        # We need at least 181 characters per line
        line = [" "] * 260
        # H = 15.0
        h_str = " 15.0"
        for j, ch in enumerate(h_str):
            line[42 + j] = ch
        # i = 5.0
        i_str = "       5.0"
        for j, ch in enumerate(i_str):
            line[147 + j] = ch
        # e = 0.15
        e_str = "      0.15"
        for j, ch in enumerate(e_str):
            line[158 + j] = ch
        # a = 2.5 (so q = 2.5 * 0.85 = 2.125)
        a_str = "         2.5"
        for j, ch in enumerate(a_str):
            line[169 + j] = ch

        cat_path = str(tmp_path / "mock_astorb.dat")
        with open(cat_path, "w") as f:
            f.write("".join(line) + "\n")

        out_path = str(tmp_path / "test_model.csv")
        stats = build_model(s3m_path, cat_path, out_path)

        assert stats["s3m_total"] > 0
        assert stats["catalog_stats"]["usable"] == 1
        assert Path(out_path).exists()

        # Verify the output is a valid model CSV
        model = read_model_csv(out_path)
        assert model["all_ss"].shape == (QX, EX, IX, HX)
        assert model["all_ss"].sum() > 0
