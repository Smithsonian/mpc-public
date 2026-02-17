"""Model and observatory code file path resolution."""

import os
from pathlib import Path


def find_model_path() -> str:
    """Locate the digest2.model.csv population model file.

    Search order:
    1. $DIGEST2_MODEL environment variable
    2. Bundled data/ directory in the installed package
    3. Repository population/ directory (editable installs)
    4. Current working directory

    Returns:
        Path to digest2.model.csv

    Raises:
        FileNotFoundError: If no model file can be found.
    """
    # 1. Environment variable
    env_path = os.environ.get("DIGEST2_MODEL")
    if env_path and Path(env_path).is_file():
        return env_path

    # 2. Bundled data directory (works for pip-installed packages)
    pkg_dir = Path(__file__).parent
    bundled_model = pkg_dir / "data" / "digest2.model.csv"
    if bundled_model.is_file():
        return str(bundled_model)

    # 3. Repository population/ directory (editable installs)
    repo_model = pkg_dir.parent.parent / "population" / "digest2.model.csv"
    if repo_model.is_file():
        return str(repo_model)

    alt_model = pkg_dir.parent.parent.parent / "population" / "digest2.model.csv"
    if alt_model.is_file():
        return str(alt_model)

    # 4. Current working directory
    cwd_model = Path.cwd() / "digest2.model.csv"
    if cwd_model.is_file():
        return str(cwd_model)

    raise FileNotFoundError(
        "Cannot find digest2.model.csv. Set DIGEST2_MODEL environment "
        "variable or ensure the file is in the current directory or "
        "the package data/ directory."
    )


def find_obscodes_path() -> str:
    """Locate the observatory codes file.

    Search order:
    1. $DIGEST2_OBSCODES environment variable
    2. Bundled data/ directory in the package
    3. Current working directory (digest2.obscodes or ObsCodes.html)

    Returns:
        Path to the observatory codes file.

    Raises:
        FileNotFoundError: If no obscodes file can be found.
    """
    # 1. Environment variable
    env_path = os.environ.get("DIGEST2_OBSCODES")
    if env_path and os.path.isfile(env_path):
        return env_path

    # 2. Current working directory
    for name in ["digest2.obscodes", "ObsCodes.html"]:
        cwd_path = Path.cwd() / name
        if cwd_path.is_file():
            return str(cwd_path)

    raise FileNotFoundError(
        "Cannot find observatory codes file. Set DIGEST2_OBSCODES "
        "environment variable or ensure digest2.obscodes or "
        "ObsCodes.html is in the current directory."
    )


def find_config_path() -> Union[str, None]:
    """Locate the MPC.config file with per-site observatory errors.

    Search order:
    1. $DIGEST2_CONFIG environment variable
    2. Bundled data/MPC.config in the package
    3. population/MPC.config in the repository
    4. Current working directory

    Returns:
        Path to MPC.config, or None if not found (not required).
    """
    # 1. Environment variable
    env_path = os.environ.get("DIGEST2_CONFIG")
    if env_path and os.path.isfile(env_path):
        return env_path

    # 2. Bundled data directory
    pkg_data = Path(__file__).parent / "data" / "MPC.config"
    if pkg_data.is_file():
        return str(pkg_data)

    # 3. Repository population directory
    pkg_dir = Path(__file__).parent
    repo_config = pkg_dir.parent.parent / "population" / "MPC.config"
    if repo_config.is_file():
        return str(repo_config)

    alt_config = pkg_dir.parent.parent.parent / "population" / "MPC.config"
    if alt_config.is_file():
        return str(alt_config)

    # 4. Current working directory
    cwd_config = Path.cwd() / "MPC.config"
    if cwd_config.is_file():
        return str(cwd_config)

    return None
