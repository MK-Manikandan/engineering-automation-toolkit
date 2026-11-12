# Load Case CSV Processor

A Python utility to extract, organize, and consolidate engineering load-case data from CSV files.

## Overview

This tool processes CSV files containing node-based engineering load data across multiple load cases. It identifies individual load cases, extracts force components (Fx, Fy, and Fz) for each node, and consolidates the extracted information into a structured output CSV file.

The utility is designed to simplify the organization and comparison of load data across multiple load cases.

## Features

- Automatically identifies load cases using the `ULC_` naming convention.
- Extracts node IDs and corresponding force components.
- Processes Fx, Fy, and Fz values for each node.
- Consolidates data from multiple load cases into a single structured CSV.
- Handles missing node data across load cases by leaving corresponding cells empty.
- Supports batch processing of multiple input CSV files.
- Automatically creates an output directory for generated files.

## Requirements

- Python 3.x
- No external Python packages required.

All modules used are part of the Python standard library.

## Project Structure

```text
load-case-csv-processor/
│
├── load_case_csv_processor.py
├── input_1.csv
├── input_2.csv
│
└── Outputs/
    ├── input_1_output.csv
    └── input_2_output.csv
```

## How It Works

The script follows these steps:

1. Reads CSV files from the script's directory.
2. Identifies load-case headers beginning with `ULC_`.
3. Skips the metadata rows associated with each load case.
4. Extracts node IDs and their corresponding Fx, Fy, and Fz values.
5. Organizes the extracted information by node and load case.
6. Generates a consolidated output CSV for each input file.
7. Saves the generated files inside the `Outputs` directory.

## Input Format

The input CSV files are expected to follow a structured format containing:

- Load-case headers in the fourth column, beginning with `ULC_`.
- Five metadata rows following each load-case header.
- Node IDs in the first column of the data section.
- Fx, Fy, and Fz values in the second, third, and fourth columns, respectively.
- Blank rows separating consecutive load-case sections.

**Note:** The script assumes a consistent input CSV structure. Files that do not follow the expected format may produce incomplete or incorrect results.

## Output Format

The generated CSV contains the following structure:

| Location | Criteria | ULC_001 | ULC_002 | ULC_003 |
|---|---|---|---|---|
| Node_1 | Fx | 125.4 | 130.2 | 118.6 |
| Node_1 | Fy | 45.2 | 48.1 | 42.7 |
| Node_1 | Fz | 210.5 | 205.3 | 215.8 |
| Node_2 | Fx | 98.3 | 102.5 | |
| Node_2 | Fy | 32.1 | 35.4 | |
| Node_2 | Fz | 150.6 | 148.2 | |

*The values above are illustrative examples.*

Each node is represented by three consecutive rows corresponding to Fx, Fy, and Fz.

## Usage

1. Place the input CSV files in the same directory as the Python script.
2. Run the script:

```bash
python3 load_case_csv_processor.py
```

3. The processed CSV files will automatically be generated inside the `Outputs` directory.

## Dependencies

This project uses only Python standard-library modules:

- `csv` – Reading and writing CSV files.
- `pathlib` – File and directory path management.

## Limitations

- Input CSV files must follow the expected structure.
- Load-case headers must begin with `ULC_` and appear in the fourth column.
- The script expects five metadata rows following each load-case header.
- Force values are extracted as strings; no numerical calculations or unit conversions are performed.
- Input CSV files should contain unique load-case identifiers.

## Author

Manikandan M

## Date

15 June 2026
