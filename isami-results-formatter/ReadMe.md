# ISAMI Element-Wise Data Converter

A Python utility to transform ISAMI `results_total` CSV output files into element-wise Excel workbooks.

## Overview

This tool converts structured ISAMI results data from CSV format into an element-wise Excel format.

It extracts element/node identifiers, load-case information, and associated result values from the input files. The extracted data is reorganized so that each element occupies a separate group of columns, making the results easier to navigate, review, and analyze.

The utility also supports batch processing of multiple input files using a centralized Excel file containing their file paths.

## Features

- Reads multiple input file paths from an Excel workbook.
- Extracts numerical results from ISAMI `results_total` CSV files.
- Identifies unique element/node identifiers.
- Extracts unique load-case names.
- Organizes results element-wise.
- Preserves result headers and associated load-case information.
- Generates separate Excel workbooks for processed input files.
- Supports batch processing of multiple input files.

## Requirements

- Python 3.x
- Microsoft Excel
- Python packages:
  - `xlwings`

Install the required package:

```bash
pip install xlwings
```

Microsoft Excel must be installed for the Excel automation functionality used by this script.

## Project Structure

```text
isami-element-wise-data-converter/
│
├── isami_element_converter.py
├── paths.xlsx
│
└── Result/
    ├── input_1_Formatted.xlsx
    ├── input_2_Formatted.xlsx
    └── ...
```

## Input Files

### 1. ISAMI Results CSV

The input files must follow the expected ISAMI `results_total` structure.

The script assumes:

- Numerical/result data starts at cell B3.
- Element/node identifiers are present in the first extracted data column.
- Load-case names are present in the second extracted data column.
- Result values follow the element and load-case identifiers.
- Result headers are located in cells D2:I2.

### 2. File Paths Workbook

An Excel workbook named `paths.xlsx` is used to specify the input file locations.

- Input file paths must be listed vertically in column A.
- The first path starts at A1.
- Additional paths can be entered in subsequent rows.

## How It Works

1. Reads the input file paths from `paths.xlsx`.
2. Opens each specified ISAMI results CSV file.
3. Extracts the result headers and data.
4. Identifies unique element/node identifiers.
5. Identifies unique load-case names.
6. Creates a new Excel workbook.
7. Organizes the extracted results element-wise.
8. Assigns each element its corresponding result data and headers.
9. Saves the formatted workbook in the specified output directory.

## Output Format

The generated Excel workbook contains:

- A serial number for each unique load case.
- Load-case names arranged horizontally.
- Element/node identifiers arranged in separate column groups.
- Corresponding result headers for each element.
- Extracted result values organized under their respective elements and load cases.

Each element occupies a group of six columns, corresponding to the six result components represented by the input headers.

## Configuration

The output directory is specified directly in the Python script.

Update the `newpath` variable to specify the desired output location:

```python
newpath = "C:/path/to/output/directory/"
```

The `paths.xlsx` file location must also be configured in the script.

## Usage

1. Create `paths.xlsx`.
2. Enter the absolute paths of the input CSV files in column A.
3. Configure the input paths workbook location in the Python script.
4. Configure the output directory.
5. Run the script:

```bash
python isami_element_converter.py
```

6. The formatted Excel workbooks will be generated in the configured output directory.

## Dependencies

- `xlwings` – Excel workbook interaction and automation.
- `sys` – Exception information and system-level utilities.
- `traceback` – Error traceback reporting.

## Limitations

- Input files must follow the expected ISAMI `results_total` structure.
- The script relies on fixed input data locations.
- The output directory must exist before execution.
- Microsoft Excel is required for xlwings automation.
- The script assumes six result components per element.
- Input file paths must be valid and accessible.

## Author

Manikandan M

## Date

14 January 2025
