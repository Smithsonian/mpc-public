"""
The code find_filter.py would search optimal threshold for selected digest2 categories using
a limit for maximum number of NEOs excluded in a given category.

Usage: python3 find_filter.py <INPUTFILE> --limit 0

Output: optimal_thresholds.json

INPUTFILE format:
a csv file with the following header:
trksub,Int1,Int2,Neo1,Neo2,MC1,MC2,Hun1,Hun2,Pho1,Pho2,MB1_1,MB1_2,Pal1,Pal2,Han1,Han2,MB2_1,MB2_2,MB3_1,MB3_2,Hil1,Hil2,JTr1,JTr2,JFC1,JFC2,class

limit - optional argument (default=0)

where trksub first character declares an NEO ('0') or non-NEO ('1')
the remaining columns are digest2 scores in a given orbit class (values 0-100) and class
represents orbit type from the digest2 code:
0 NEO
1 Mars Crosser
2 Hungarias
3 Phocaeas
4 Inner Main Belt
5 Hansa
6 Pallas
7 Central Main Belt
8 Outer Main Belt
9 Hilda
10 Jupiter Trojan
11 Jupiter Family Comet
12 MPC interesting (q<1.3 AU OR e>0.5 OR i>=40 deg OR Q>10)

"""

import pandas as pd
import json
import argparse
import os



# Define the columns to be analyzed in threshold calculations
ANALYZED_COLUMNS = {'trksub', 'class', 'Neo2', 'Neo1', 'Han2', 'Han1', 'Int2', 'Int1',
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
    missing_columns = ANALYZED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Error: Missing required columns: {missing_columns}")

    return df

def find_optimal_thresholds(input_file, limit=0, output_file="optimal_thresholds.json"):
    df = validate_input_file(input_file)
    optimal_thresholds = {}

    # Only check columns that are NOT in ANALYZED_COLUMNS
    columns_to_check = df.columns.difference(ANALYZED_COLUMNS)

    for col in columns_to_check:
        thresholds = []
        for i in range(0, 100):
            count0 = df[(df[col] > i) & (df['class'] == 0)].shape[0]
            count1 = df[(df[col] > i) & (df['class'] != 0)].shape[0]
            if count0 <= limit:
                thresholds.append((f'>{i}', count1, count0))
        for i in range(0, 100):
            count0 = df[(df[col] < i) & (df['class'] == 0)].shape[0]
            count1 = df[(df[col] < i) & (df['class'] != 0)].shape[0]
            if count0 <= limit:
                thresholds.append((f'<{i}', count1, count0))

        if thresholds:
            optimal = max(thresholds, key=lambda x: (x[1], -x[2]))
            optimal_thresholds[col] = optimal

    with open(output_file, 'w') as f:
        json.dump(optimal_thresholds, f, indent=4)

    print(f"Optimal thresholds saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find optimal thresholds from a CSV file.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("--limit", type=int, help="Maximum NEO count limit per digest2 category.", default=0)
    args = parser.parse_args()

    try:
        find_optimal_thresholds(args.input_file, args.limit)
    except Exception as e:
        print(f"Error: {e}")