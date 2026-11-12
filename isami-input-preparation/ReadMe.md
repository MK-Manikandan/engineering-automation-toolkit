# ISAMI Input File Automation

A collection of Python utilities to automate the preparation and modification of ISAMI input Excel workbooks.

## Scripts

### 1. ULC/CLC Copy-Paste

`ulc_clc_copy_paste.py`

- Copies ULC and CLC data from predefined source workbooks.
- Updates corresponding ULC List and CLC List sheets in multiple target workbooks.
- Updates the LCSet sheet using the load-case number ranges.
- Supports different model configurations through a centralized paths workbook.

### 2. ISAMI BDF Path Updater

`isami_bdf_path_updater.py`

- Updates the BDF model path in the `Analyses` sheet.
- Clears the existing OP2 model path.
- Supports standard and PS model configurations.
- Processes multiple ISAMI input workbooks using a centralized paths workbook.

## Requirements

- Python 3.x
- Microsoft Excel
- `xlwings`

Install the dependency:

```bash
pip install xlwings
```

## Usage

1. Configure the source file paths in the respective scripts.
2. Update the location of the `paths.xlsx` workbook.
3. Enter the target workbook paths and required configurations in `paths.xlsx`.
4. Run the required script:

```bash
python ulc_clc_copy_paste.py
```

or

```bash
python isami_bdf_path_updater.py
```

## Author

Manikandan M

**Date:** 20 January 2025
