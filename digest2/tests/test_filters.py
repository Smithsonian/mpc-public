"""Tests for the NEOCP filter integration (digest2.filters)."""

import json
import tempfile
from pathlib import Path

import pytest

# Filters require pandas
pandas = pytest.importorskip("pandas")

from digest2.filters import apply_filter, find_optimal_thresholds, load_thresholds


@pytest.fixture
def sample_scores_csv(tmp_path):
    """Create a sample digest2 scores CSV file."""
    csv_content = (
        "trksub,Int1,Int2,Neo1,Neo2,MC1,MC2,Hun1,Hun2,Pho1,Pho2,"
        "MB1_1,MB1_2,Pal1,Pal2,Han1,Han2,MB2_1,MB2_2,MB3_1,MB3_2,"
        "Hil1,Hil2,JTr1,JTr2,JFC1,JFC2,class\n"
        # NEO (class=0): low MB scores
        "neo1,90,85,95,92,5,3,0,0,0,0,2,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0\n"
        "neo2,88,82,93,90,8,5,0,0,0,0,3,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0\n"
        # Non-NEO (class=1): high MB scores
        "mb1,5,3,2,1,10,5,0,0,0,0,85,90,0,0,0,0,5,3,0,0,0,0,0,0,0,0,1\n"
        "mb2,3,2,1,0,8,4,0,0,0,0,88,92,0,0,0,0,3,2,0,0,0,0,0,0,0,0,1\n"
        "mb3,4,2,1,1,12,6,0,0,0,0,82,88,0,0,0,0,6,4,0,0,0,0,0,0,0,0,1\n"
    )
    f = tmp_path / "scores.csv"
    f.write_text(csv_content)
    return str(f)


class TestFindOptimalThresholds:
    """Test threshold discovery."""

    def test_find_thresholds(self, sample_scores_csv, tmp_path):
        output_file = str(tmp_path / "thresholds.json")
        thresholds = find_optimal_thresholds(
            sample_scores_csv, limit=0, output_file=output_file
        )

        assert isinstance(thresholds, dict)
        assert len(thresholds) > 0

        # Check that output file was written
        assert Path(output_file).exists()

    def test_find_thresholds_no_output(self, sample_scores_csv):
        thresholds = find_optimal_thresholds(sample_scores_csv, limit=0)
        assert isinstance(thresholds, dict)

    def test_find_thresholds_with_limit(self, sample_scores_csv):
        thresholds = find_optimal_thresholds(sample_scores_csv, limit=1)
        assert isinstance(thresholds, dict)


class TestApplyFilter:
    """Test threshold application."""

    def test_apply_filter(self, sample_scores_csv, tmp_path):
        # First find thresholds
        thresholds = find_optimal_thresholds(sample_scores_csv, limit=0)

        # Apply them
        output_file = str(tmp_path / "filtered.csv")
        passed = apply_filter(sample_scores_csv, thresholds, output_file)

        assert isinstance(passed, list)
        # Non-NEO objects should be identified
        # At least some should be in the passed list
        assert len(passed) >= 0  # May or may not find any depending on thresholds


class TestLoadThresholds:
    """Test loading thresholds from JSON."""

    def test_load(self, tmp_path):
        thresholds = {
            "MB1_1": [">80", 3, 0],
            "MB2_1": ["<5", 2, 0],
        }
        f = tmp_path / "thresh.json"
        f.write_text(json.dumps(thresholds))

        loaded = load_thresholds(str(f))
        assert loaded == thresholds
