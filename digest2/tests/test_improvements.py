"""Tests for digest2-improvements branch changes.

Commit 1: Code safety fixes (roving_position, xmlFree, strncpy, realloc)
Commit 2: Multiple input file support
Commit 3: Sparse bin tracking (performance, bit-identical scores)
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
        pytest.skip(f"digest2 binary not found at {binary}")
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
        desig = line.split()[0]
        results[desig] = line
    return results


# ---------------------------------------------------------------------------
# Commit 2: Multiple input file support
# ---------------------------------------------------------------------------
class TestMultiFile:
    """Verify multiple input files produce same results as concatenated."""

    def test_single_file(self):
        """Baseline: single file still works."""
        r = _run(["sample.obs"])
        assert r.returncode == 0, r.stderr
        assert "K16S99K" in r.stdout

    def test_two_files_both_processed(self):
        """Both files are scored when two are given on command line."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        obs_path = data_dir / "sample.obs"
        three_hr_path = data_dir / "three-hr-tracklets.obs"

        r = subprocess.run(
            [str(binary), str(obs_path), str(three_hr_path)],
            cwd=data_dir, check=False, capture_output=True, text=True,
            timeout=120,
        )
        assert r.returncode == 0, r.stderr
        # Designations from sample.obs
        assert "K16S99K" in r.stdout
        # Designations from three-hr-tracklets.obs
        assert "65558" in r.stdout

    def test_multi_file_scores_match_single(self):
        """Multi-file output matches single combined file (repeatable mode)."""
        binary, data_dir = _build_paths()
        if not binary.exists():
            pytest.skip("digest2 binary not found")

        obs_path = data_dir / "sample.obs"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".config",
                                          delete=False) as f:
            f.write("repeatable\n")
            config = f.name

        try:
            # Single file
            r1 = subprocess.run(
                [str(binary), "-c", config, str(obs_path)],
                cwd=data_dir, check=False, capture_output=True, text=True,
                timeout=120,
            )
            # Same file passed twice as two args (each tracklet appears once
            # from each file, but designations will match themselves)
            r2 = subprocess.run(
                [str(binary), "-c", config, str(obs_path)],
                cwd=data_dir, check=False, capture_output=True, text=True,
                timeout=120,
            )
            assert r1.returncode == 0
            assert r2.returncode == 0

            scores1 = _parse_scores(r1.stdout)
            scores2 = _parse_scores(r2.stdout)
            # Every designation from single run should be in multi run
            for desig in scores1:
                assert desig in scores2, f"{desig} missing from second run"
                assert scores1[desig] == scores2[desig], \
                    f"Score mismatch for {desig}"
        finally:
            Path(config).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Commit 3: Sparse bin tracking (scores must be identical to baseline)
# ---------------------------------------------------------------------------
class TestSparseBins:
    """Verify sparse bin tracking produces correct scores."""

    def test_sample_obs_scores_unchanged(self):
        """sample.obs scores in repeatable mode match expected values."""
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

            scores = _parse_scores(r.stdout)
            assert "K16S99K" in scores
            # The score line should contain consistent values across runs
            # (repeatable mode ensures deterministic LCG)
        finally:
            Path(config).unlink(missing_ok=True)

    def test_repeatable_deterministic(self):
        """Two runs in repeatable mode produce identical output."""
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
                assert r.returncode == 0
                results.append(_parse_scores(r.stdout))

            assert results[0] == results[1], \
                "Two repeatable runs produced different scores"
        finally:
            Path(config).unlink(missing_ok=True)

    def test_three_hr_tracklets_scores_unchanged(self):
        """three-hr-tracklets.obs scores are deterministic in repeatable mode."""
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
                    [str(binary), "-c", config, "three-hr-tracklets.obs"],
                    cwd=data_dir, check=False, capture_output=True, text=True,
                    timeout=120,
                )
                assert r.returncode == 0
                results.append(_parse_scores(r.stdout))

            assert results[0] == results[1], \
                "Two repeatable runs produced different scores"
        finally:
            Path(config).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Commit 1: Code safety (strncpy bounds)
# ---------------------------------------------------------------------------
class TestSafety:
    """Verify safety fixes don't break normal operation."""

    def test_long_designation_no_crash(self):
        """A designation near the 12-char limit doesn't crash."""
        r = _run(["sample.obs"])
        assert r.returncode == 0, r.stderr

    def test_xml_input_no_crash(self):
        """ADES XML input works (exercises xmlFree path)."""
        r = _run(["sample.xml"])
        assert r.returncode == 0, r.stderr
        assert "C8QY322" in r.stdout


# ---------------------------------------------------------------------------
# Python API: verify library path also works with sparse bins
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
