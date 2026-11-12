# Excel Note Automation

A collection of Python scripts to automate data handling using Excel cell notes.

## Scripts

### 1. Copy Notes to Cells

`copy_notes_to_cells.py`

- Scans all worksheets in an Excel workbook.
- Identifies cells containing notes.
- Copies the note text into the corresponding cell value.
- Saves the modified workbook.

### 2. Search Files from Notes

`search_files_from_notes.py`

- Searches for Excel workbooks within a specified directory and its subdirectories.
- Extracts workbook names and cell references from Excel notes.
- Retrieves data from the referenced external workbooks and cell ranges.
- Copies the retrieved data into the corresponding cells in the main workbook.
- Saves the modified workbook.

## Requirements

- Python 3.x
- Microsoft Excel
- `xlwings`

Install the dependency:

```bash
pip install xlwings
```

## Usage

Update the input file paths and directory locations in the respective scripts.

Run either script:

```bash
python copy_notes_to_cells.py
```

```bash
python search_files_from_notes.py
```

## Author

Manikandan M
