import os
import re
import xlwings as xw

def find_all_xlsx_files(base_path):
    """Walk through folders and store all .xlsx files with their full paths."""
    file_map = {}
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".xlsx"):
                file_map[file.lower()] = os.path.join(root, file)
    return file_map

def extract_file_and_range(note_text):
    """Extract file name and Excel cell/range using regex."""
    file_match = re.search(r"([\w\s\-\.]+\.xlsx)", note_text, re.IGNORECASE)
    range_match = re.search(r"\b([A-Za-z]+\d+(:[A-Za-z]+\d+)?)\b", note_text)

    filename = file_match.group(1) if file_match else None
    cell_range = range_match.group(1) if range_match else None
    return filename, cell_range

def copy_from_external_and_paste(target_cell, external_path, source_range):
    try:
        wb_ext = xw.Book(external_path)
        sheet_ext = wb_ext.sheets[0]
        data = sheet_ext.range(source_range).value
        target_cell.value = data
        wb_ext.close()
    except Exception as e:
        print(f"Error reading from {external_path} range {source_range}: {e}")

def process_excel_notes(main_file, base_folder):
    file_map = find_all_xlsx_files(base_folder)

    app = None
    wb_main = None
    try:
        app = xw.App(visible=False)
        wb_main = app.books.open(main_file)
        for sheet in wb_main.sheets:
            used_range = sheet.used_range
            for row in used_range.rows:
                for cell in row:
                    note = cell.note
                    if note:
                        note_text = note.text
                        filename, cell_range = extract_file_and_range(note_text)
                        if filename and cell_range:
                            file_path = file_map.get(filename.lower())
                            if file_path:
                                copy_from_external_and_paste(cell, file_path, cell_range)
                            else:
                                print(f"File NOT found: '{filename}' referenced in cell {cell.address}")
        wb_main.save()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if wb_main:
            wb_main.close()
        if app:
            app.quit()

# Example usage:
main_excel = "main.xlsx"  # Your file with notes
search_root = "C:/Users/YourName/Documents"  # Folder to search in
process_excel_notes(main_excel, search_root)

'''
Manikandan M
'''
