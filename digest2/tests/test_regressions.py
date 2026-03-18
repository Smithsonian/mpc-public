"""Regression tests for combined digest2 improvements.

Covers:
- Code safety fixes (strncpy bounds, roving_position thread safety, realloc growth)
- Memory leak fixes (free_optical, xmlFree for ADES fields)
- Multiple input file support (mix .obs and .xml)
- Sparse bin tracking (bit-identical scores, deterministic in repeatable mode)
- Python library API path with sparse bins
"""
import subprocess
import tempfile
from pathlib import Path

import pytest


def _build_paths():
    project_dir = Path(__file__).resolve().parents[1]
    data_dir = project_dir / "digest2"
    binary = data_dir / "digest2"
    return binary, data_dir


def _run(args, cwd=None, timeout=120):
    binary, data_dir = _build_paths()
    if not binary.exists():
        pytest.skip(f"digest2 binary not found at {binary} (run: cd digest2/digest2 && make)")
    if cwd is None:
        cwd = data_dir
    return subprocess.run(
        [str(binary)] + list(args),
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _parse_scores(output):
    """Parse digest2 output into {designation: full_line} dict."""
    results = {}
    for line in output.strip().splitlines():
        if not line or "Desig" in line or line.startswith("-"):
            continue
        parts = line.split()
        if parts:
            results[parts[0]] = line
    return results


# ---------------------------------------------------------------------------
# Multiple input file support
# ---------------------------------------------------------------------------
class TestMultiFile:
    """Verify multiple input files produce the expected results."""

    def test_single_file(self):
        """Baseline: single .obs file still works."""
        r = _run(["sample.obs"])
        assert r.returncode == 0, r.stderr
        assert "K16S99K" in r.stdout

    def test_single_xml_file(self):
        """Baseline: single .xml file still works."""
        r = _run(["sample.xml"])
        assert r.returncode == 0, r.stderr
        assert "C8QY322" in r.stdout

    def test_two_obs_files_both_processed(self):
        """Both .obs files are scored when given on command line."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        obs_path = data_dir / "sample.obs"
        three_hr_path = data_dir / "three-hr-tracklets.obs"
        if not three_hr_path.exists():
            pytest.skip("three-hr-tracklets.obs not found")

        r = subprocess.run(
            [str(binary), str(obs_path), str(three_hr_path)],
            cwd=data_dir, check=False, capture_output=True, text=True,
            timeout=120,
        )
        assert r.returncode == 0, r.stderr
        assert "K16S99K" in r.stdout
        assert "65558" in r.stdout

    def test_mixed_format_files(self):
        """Mixed .obs and .xml files in one invocation both produce output."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        obs_path = data_dir / "sample.obs"
        xml_path = data_dir / "sample.xml"
        if not xml_path.exists():
            pytest.skip("sample.xml not found")

        r = subprocess.run(
            [str(binary), str(obs_path), str(xml_path)],
            cwd=data_dir, check=False, capture_output=True, text=True,
            timeout=120,
        )
        assert r.returncode == 0, r.stderr
        assert "K16S99K" in r.stdout
        assert "C8QY322" in r.stdout

    def test_multi_file_scores_match_single(self):
        """Passing the same file twice gives identical per-tracklet scores."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        obs_path = data_dir / "sample.obs"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".config",
                                         delete=False) as f:
            f.write("repeatable\n")
            config = f.name

        try:
            # Single file run
            r1 = subprocess.run(
                [str(binary), "-c", config, str(obs_path)],
                cwd=data_dir, check=False, capture_output=True, text=True,
                timeout=120,
            )
            # Same file passed twice as two args — each tracklet appears once per file
            r2 = subprocess.run(
                [str(binary), "-c", config, str(obs_path), str(obs_path)],
                cwd=data_dir, check=False, capture_output=True, text=True,
                timeout=120,
            )
            assert r1.returncode == 0, r1.stderr
            assert r2.returncode == 0, r2.stderr

            scores1 = _parse_scores(r1.stdout)
            scores2 = _parse_scores(r2.stdout)
            # Every designation from single run should be in multi run with same scores
            for desig in scores1:
                assert desig in scores2, f"{desig} missing from two-file run"
                assert scores1[desig] == scores2[desig], \
                    f"Score mismatch for {desig}: {scores1[desig]!r} vs {scores2[desig]!r}"
        finally:
            Path(config).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Sparse bin tracking — scores must be deterministic in repeatable mode
# ---------------------------------------------------------------------------
class TestSparseBins:
    """Verify sparse bin tracking produces correct and deterministic scores."""

    def test_repeatable_deterministic_sample_obs(self):
        """Two repeatable runs on sample.obs produce identical output."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".config",
                                         delete=False) as f:
            f.write("repeatable\n")
            config = f.name

        try:
            results = []
            for _ in range(2):
                r = subprocess.run(
                    [str(binary), "-c", config, "sample.obs"],
                    cwd=data_dir, check=False, capture_output=True, text=True,
                    timeout=120,
                )
                assert r.returncode == 0, r.stderr
                results.append(_parse_scores(r.stdout))

            assert results[0] == results[1], \
                "Two repeatable runs on sample.obs produced different scores"
        finally:
            Path(config).unlink(missing_ok=True)

    def test_repeatable_deterministic_three_hr(self):
        """Two repeatable runs on three-hr-tracklets.obs produce identical output."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        three_hr = data_dir / "three-hr-tracklets.obs"
        if not three_hr.exists():
            pytest.skip("three-hr-tracklets.obs not found")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".config",
                                         delete=False) as f:
            f.write("repeatable\n")
            config = f.name

        try:
            results = []
            for _ in range(2):
                r = subprocess.run(
                    [str(binary), "-c", config, str(three_hr)],
                    cwd=data_dir, check=False, capture_output=True, text=True,
                    timeout=120,
                )
                assert r.returncode == 0, r.stderr
                results.append(_parse_scores(r.stdout))

            assert results[0] == results[1], \
                "Two repeatable runs on three-hr-tracklets.obs produced different scores"
        finally:
            Path(config).unlink(missing_ok=True)

    def test_sample_obs_contains_expected_designation(self):
        """sample.obs scores in repeatable mode contain K16S99K."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".config",
                                         delete=False) as f:
            f.write("repeatable\n")
            config = f.name

        try:
            r = subprocess.run(
                [str(binary), "-c", config, "sample.obs"],
                cwd=data_dir, check=False, capture_output=True, text=True,
                timeout=120,
            )
            assert r.returncode == 0, r.stderr
            assert "K16S99K" in r.stdout
        finally:
            Path(config).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Safety fixes — exercise the fixed code paths without crashing
# ---------------------------------------------------------------------------
class TestSafety:
    """Verify safety fixes don't break normal operation."""

    def test_normal_obs_no_crash(self):
        """Normal .obs input doesn't crash (exercises strncpy fix)."""
        r = _run(["sample.obs"])
        assert r.returncode == 0, r.stderr

    def test_xml_input_no_crash(self):
        """ADES XML input works (exercises free_optical / xmlFree fix)."""
        r = _run(["sample.xml"])
        assert r.returncode == 0, r.stderr
        assert "C8QY322" in r.stdout

    def test_xml_scores_plausible(self):
        """XML input produces scores in valid range 0-100."""
        r = _run(["sample.xml"])
        assert r.returncode == 0, r.stderr
        scores = _parse_scores(r.stdout)
        assert len(scores) > 0, "No scores produced from sample.xml"
        for desig, line in scores.items():
            parts = line.split()
            # After designation and RMS, all fields should be numeric
            for field in parts[2:]:
                # Strip parenthetical possibilities like "(MC" or "13)"
                if field.startswith("(") or field.endswith(")"):
                    continue
                try:
                    val = float(field)
                    assert 0 <= val <= 100, f"Score {val} out of range for {desig}"
                except ValueError:
                    pass  # Non-numeric fields (e.g., "Desig.") are OK


# ---------------------------------------------------------------------------
# Python library API — verify d2lib.c path works correctly
# ---------------------------------------------------------------------------
class TestLibraryAPI:
    """Verify the Python extension (d2lib.c path) works with sparse bins."""

    def test_classify_returns_scores(self, model_path, obscodes_path,
                                     sample_obs_path):
        """classify() via Python API returns valid scores."""
        from digest2 import classify
        results = classify(sample_obs_path,
                           model_path=model_path,
                           obscodes_path=obscodes_path)
        assert len(results) > 0
        for r in results:
            assert r.designation is not None
            assert r.raw['NEO'] is not None
            assert 0 <= r.raw['NEO'] <= 100
            assert 0 <= r.noid['NEO'] <= 100

    def test_classify_repeatable(self, model_path, obscodes_path,
                                 sample_obs_path):
        """Two classify() calls in repeatable mode give identical scores."""
        from digest2 import classify
        r1 = classify(sample_obs_path, model_path=model_path,
                      obscodes_path=obscodes_path, repeatable=True)
        r2 = classify(sample_obs_path, model_path=model_path,
                      obscodes_path=obscodes_path, repeatable=True)
        assert len(r1) == len(r2)
        for a, b in zip(r1, r2):
            assert a.designation == b.designation
            assert a.raw['NEO'] == b.raw['NEO']
            assert a.noid['NEO'] == b.noid['NEO']

    def test_classify_xml(self, model_path, obscodes_path, sample_xml_path):
        """classify() on ADES XML returns valid scores (exercises XML path)."""
        from digest2 import classify
        results = classify(sample_xml_path,
                           model_path=model_path,
                           obscodes_path=obscodes_path)
        assert len(results) > 0
        for r in results:
            assert r.designation is not None
            assert 0 <= r.noid['NEO'] <= 100
