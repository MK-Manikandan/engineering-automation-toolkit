import xlwings as xw
import os

def copy_notes_to_values(filepath):
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return

    app = None
    wb = None
    try:
        app = xw.App(visible=False)
        wb = app.books.open(filepath)
        for sheet in wb.sheets:
            used_range = sheet.used_range
            for row in used_range.rows:
                for cell in row:
                    if cell.note:  # Note exists
                        cell.value = cell.note.text  # Use note's text
        wb.save()
        print("Notes copied to cell values successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if wb:
            wb.close()
        if app:
            app.quit()

