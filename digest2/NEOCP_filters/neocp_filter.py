"""
The code neocp_filter.py takes the threshold json file and a digest2 results and selects
designations (trksubs) that are assumed to be non-NEOs.

Usage: python3 neocp_filter.py <INPUTFILE> <JSON_MODEL>
Output: a file (filtered_pass.csv) with the resulting trksub and print on screen
"""

import pandas as pd
import json
import argparse
import os

# Define the columns to check for filtering
EXCLUDED_COLUMNS = {'trksub', 'class', 'Neo2', 'Neo1', 'Han2', 'Han1', 'Int2', 'Int1', 
                    'Hil1', 'Hil2', 'Pho1', 'Pho2', 'MC1', 'MC2'}

def validate_input_file(input_file):
    """Validates if the input CSV file exists, is readable, and has the required columns."""
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Error: File '{input_file}' not found.")

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")

    # Check if all expected columns exist
    missing_columns = EXCLUDED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Error: Missing required columns: {missing_columns}")

    return df

def filter_and_output_passed_entries(input_file, thresholds_file, output_file="filtered_pass.csv"):
    """Reads optimal thresholds, filters data that meets conditions, and saves 'trksub' values."""
    
    if not os.path.isfile(thresholds_file):
        raise FileNotFoundError(f"Error: Thresholds file '{thresholds_file}' not found.")
    
    with open(thresholds_file, 'r') as f:
        optimal_thresholds = json.load(f)

    df = validate_input_file(input_file)

    # Only apply thresholds on the specified columns
    columns_to_check = df.columns.difference(EXCLUDED_COLUMNS)

    combined_condition = None
    for col in columns_to_check:
        if col in optimal_thresholds:
            threshold, _, _ = optimal_thresholds[col]
            if threshold.startswith('>'):
                value = int(threshold[1:])
                condition = df[col] > value
            elif threshold.startswith('<'):
                value = int(threshold[1:])
                condition = df[col] < value
            if combined_condition is None:
                combined_condition = condition
            else:
                combined_condition |= condition

    passed_df = df[combined_condition] if combined_condition is not None else df.iloc[0:0]

    # Select only 'trksub' column
    output_df = passed_df[['trksub']]

    # Save the filtered 'trksub' values to a CSV file
    output_df.to_csv(output_file, index=False, header=False)

    # Print the results (WITHOUT HEADER)
    for trksub in output_df['trksub']:
        print(trksub)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Output entries that pass optimal thresholds.")
    parser.add_argument("input_file", type=str, help="Path to the new input CSV file.")
    parser.add_argument("thresholds_file", type=str, help="Path to the optimal thresholds JSON file.")
    args = parser.parse_args()

    try:
        filter_and_output_passed_entries(args.input_file, args.thresholds_file)
    except Exception as e:
        print(f"Error: {e}")
