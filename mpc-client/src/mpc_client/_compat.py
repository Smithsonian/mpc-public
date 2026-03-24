"""Lazy-import helper for optional pandas dependency."""

from __future__ import annotations


def require_pandas():
    """Import and return pandas, raising a helpful error if not installed."""
    try:
        import pandas as pd

        return pd
    except ImportError:
        raise ImportError(
            "pandas is required for this method. "
            "Install it with: pip install mpc-client[dataframe]"
        )
