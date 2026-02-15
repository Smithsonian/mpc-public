"""NEOCP filter tools for identifying likely non-NEO tracklets.

Integrated from the NEOCP_filters/ scripts (find_filter.py and
neocp_filter.py). These functions work with digest2 scoring output
to derive and apply thresholds that filter out non-NEO objects.
"""

import json
from typing import Dict, List, Optional, Set, Tuple


# Columns excluded from threshold analysis (always kept as-is)
EXCLUDED_COLUMNS = frozenset({
    "trksub", "class", "Neo2", "Neo1", "Han2", "Han1", "Int2", "Int1",
    "Hil1", "Hil2", "Pho1", "Pho2", "MC1", "MC2",
})


def find_optimal_thresholds(
    input_file: str,
    limit: int = 0,
    output_file: Optional[str] = None,
) -> dict:
    """Derive optimal per-class thresholds from labeled digest2 output.

    Searches for threshold values in each non-excluded column that maximize
    the count of non-NEOs identified while keeping the count of misclassified
    NEOs at or below `limit`.

    Args:
        input_file: Path to CSV with digest2 scores and a 'class' column
            (0 = NEO, non-zero = non-NEO).
        limit: Maximum number of NEOs allowed to be misclassified per
            category (default 0 = no NEOs misclassified).
        output_file: If provided, write thresholds to this JSON file.

    Returns:
        Dict mapping column name -> (threshold_str, non_neo_count, neo_count).
        threshold_str is like ">50" or "<10".
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for filter functions. "
            "Install with: pip install digest2[filters]"
        )

    df = pd.read_csv(input_file)

    # Validate required columns
    missing = EXCLUDED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    optimal_thresholds = {}
    columns_to_check = df.columns.difference(EXCLUDED_COLUMNS)

    for col in columns_to_check:
        thresholds = []

        # Check > thresholds
        for i in range(0, 100):
            count_neo = df[(df[col] > i) & (df["class"] == 0)].shape[0]
            count_nonneo = df[(df[col] > i) & (df["class"] != 0)].shape[0]
            if count_neo <= limit:
                thresholds.append((f">{i}", count_nonneo, count_neo))

        # Check < thresholds
        for i in range(0, 100):
            count_neo = df[(df[col] < i) & (df["class"] == 0)].shape[0]
            count_nonneo = df[(df[col] < i) & (df["class"] != 0)].shape[0]
            if count_neo <= limit:
                thresholds.append((f"<{i}", count_nonneo, count_neo))

        if thresholds:
            # Pick the threshold that catches the most non-NEOs
            optimal = max(thresholds, key=lambda x: (x[1], -x[2]))
            optimal_thresholds[col] = optimal

    if output_file:
        with open(output_file, "w") as f:
            json.dump(optimal_thresholds, f, indent=4)

    return optimal_thresholds


def apply_filter(
    input_file: str,
    thresholds: dict,
    output_file: Optional[str] = None,
) -> list:
    """Apply thresholds to identify likely non-NEO tracklets.

    Any tracklet matching ANY threshold condition is considered a likely
    non-NEO (conditions are OR'd together).

    Args:
        input_file: Path to CSV with digest2 scores.
        thresholds: Dict from find_optimal_thresholds() or loaded from JSON.
            Format: {column_name: (threshold_str, count, count), ...}
            or {column_name: [threshold_str, count, count], ...}
        output_file: If provided, write filtered trksub values to this CSV.

    Returns:
        List of trksub identifiers that are likely non-NEOs.
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for filter functions. "
            "Install with: pip install digest2[filters]"
        )

    df = pd.read_csv(input_file)
    columns_to_check = df.columns.difference(EXCLUDED_COLUMNS)

    combined_condition = None
    for col in columns_to_check:
        if col in thresholds:
            threshold_info = thresholds[col]
            threshold_str = threshold_info[0] if isinstance(threshold_info, (list, tuple)) else threshold_info

            if threshold_str.startswith(">"):
                value = int(threshold_str[1:])
                condition = df[col] > value
            elif threshold_str.startswith("<"):
                value = int(threshold_str[1:])
                condition = df[col] < value
            else:
                continue

            if combined_condition is None:
                combined_condition = condition
            else:
                combined_condition |= condition

    if combined_condition is not None:
        passed_df = df[combined_condition]
    else:
        passed_df = df.iloc[0:0]

    result = passed_df["trksub"].tolist()

    if output_file:
        passed_df[["trksub"]].to_csv(output_file, index=False, header=False)

    return result


def load_thresholds(filepath: str) -> dict:
    """Load thresholds from a JSON file.

    Args:
        filepath: Path to the JSON thresholds file.

    Returns:
        Dict of thresholds suitable for apply_filter().
    """
    with open(filepath, "r") as f:
        return json.load(f)
