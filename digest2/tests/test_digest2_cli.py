import subprocess
from pathlib import Path


def _build_paths():
    """Return (binary_path, data_dir) relative to this test file."""
    project_dir = Path(__file__).resolve().parents[1]  # digest2/
    data_dir = project_dir / "digest2"
    binary = data_dir / "digest2"
    return binary, data_dir


def _run_digest2(input_name: str) -> subprocess.CompletedProcess:
    """Run digest2 on a given input file name residing in data_dir."""
    binary, data_dir = _build_paths()
    if not binary.exists():
        # Allow running the test suite before building locally.
        import pytest

        pytest.skip(f"digest2 binary not found at {binary}")
    return subprocess.run(
        [str(binary), input_name],
        cwd=data_dir,
        check=False,
        capture_output=True,
        text=True,
    )


def test_sample_obs_runs_and_reports_designation():
    result = _run_digest2("sample.obs")
    assert result.returncode == 0, result.stderr
    assert "Desig." in result.stdout
    assert "K16S99K" in result.stdout


def test_sample_xml_runs_and_reports_designation():
    result = _run_digest2("sample.xml")
    assert result.returncode == 0, result.stderr
    assert "Desig." in result.stdout
    assert "C8QY322" in result.stdout


def test_three_hr_tracklets_runs_and_reports_first_object():
    result = _run_digest2("three-hr-tracklets.obs")
    assert result.returncode == 0, result.stderr
    assert "Desig." in result.stdout
    # One of the first designations in the output listing.
    assert "65558" in result.stdout
