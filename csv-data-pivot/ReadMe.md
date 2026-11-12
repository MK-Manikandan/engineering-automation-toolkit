# Results Total Element-Wise Converter

A Python script to convert `results_total.csv` data from load-case-wise format to element-wise format.

## Features

- Reads engineering results from a CSV file.
- Extracts unique element IDs and load-case names.
- Organizes result components element-wise.
- Allows exclusion of unwanted load cases.
- Generates a reorganized CSV output.

## Requirements

- Python 3.x
- No external dependencies.

## Configuration

Update the following parameters in the script:

- `path` – Input CSV file location.
- `col_count` – Number of columns per element.
- `elem_count` – Number of elements.
- `lc_count` – Number of load cases.

Modify the load-case exclusion conditions as required.

## Usage

Run the script:

```bash
python results_total_converter.py
```

The output is saved as `output.csv` in the current working directory.

## Author

Manikandan M

**Date:** 23 July 2025
