"""Shared fixtures for digest2 tests."""

import os
from pathlib import Path

import pytest


@pytest.fixture
def digest2_dir():
    """Return the path to the digest2 package root."""
    return Path(__file__).parent.parent


@pytest.fixture
def model_path(digest2_dir):
    """Return path to the population model CSV."""
    return str(digest2_dir / "population" / "digest2.model.csv")


@pytest.fixture
def obscodes_path(digest2_dir):
    """Return path to the observatory codes file."""
    p = digest2_dir / "digest2" / "digest2.obscodes"
    if not p.exists():
        pytest.skip("digest2.obscodes not found (run: curl -o digest2/digest2.obscodes "
                     "https://minorplanetcenter.net/iau/lists/ObsCodes.html)")
    return str(p)


@pytest.fixture
def sample_obs_path(digest2_dir):
    """Return path to sample.obs."""
    return str(digest2_dir / "digest2" / "sample.obs")


@pytest.fixture
def sample_xml_path(digest2_dir):
    """Return path to sample.xml."""
    p = digest2_dir / "digest2" / "sample.xml"
    if not p.exists():
        pytest.skip("sample.xml not found")
    return str(p)


@pytest.fixture
def mpc_config_path(digest2_dir):
    """Return path to the MPC.config in population/."""
    return str(digest2_dir / "population" / "MPC.config")


@pytest.fixture
def empty_config_path(tmp_path):
    """Return path to an empty config file."""
    p = tmp_path / "empty.config"
    p.write_text("# empty config\n")
    return str(p)
