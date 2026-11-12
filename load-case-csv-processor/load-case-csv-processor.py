import csv
from pathlib import Path


def read_csv(csv_path: Path):
    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as infile:
        return list(csv.reader(infile))


def is_blank_row(row):
    return not any(cell.strip() for cell in row)


def extract_load_cases(rows):
    """
    Extracts all load case data from the input CSV.

    Returns:
        load_cases: list[str]
        node_data: {
            node_id: {
                load_case: {
                    "fx": value,
                    "fy": value,
                    "fz": value
                }
            }
        }
    """
    load_cases = []
    node_data = {}

    row_idx = 0

    while row_idx < len(rows):

        row = rows[row_idx]

        # Detect load case header row
        if len(row) >= 4 and row[3].strip().startswith("ULC_"):

            load_case = row[3].strip()
            load_cases.append(load_case)

            # Skip the 6 metadata rows
            row_idx += 5

            # Read data rows until blank separator row
            while row_idx < len(rows):

                current_row = rows[row_idx]

                if is_blank_row(current_row):
                    break

                if len(current_row) < 4:
                    row_idx += 1
                    continue

                node_id = current_row[0].strip()

                if not node_id:
                    row_idx += 1
                    continue

                fx = current_row[1].strip()
                fy = current_row[2].strip()
                fz = current_row[3].strip()

                node_data.setdefault(node_id, {})
                node_data[node_id][load_case] = {
                    "fx": fx,
                    "fy": fy,
                    "fz": fz,
                }

                row_idx += 1

        row_idx += 1

    return load_cases, node_data


def build_output_rows(load_cases, node_data):
    output_rows = []

    header = ["Location", "Criteria", *load_cases]
    output_rows.append(header)

    for node_id in sorted(node_data.keys()):

        fx_row = [node_id, "Fx"]
        fy_row = [node_id, "Fy"]
        fz_row = [node_id, "Fz"]

        for load_case in load_cases:

            values = node_data[node_id].get(load_case)

            if values:
                fx_row.append(values["fx"])
                fy_row.append(values["fy"])
                fz_row.append(values["fz"])
            else:
                fx_row.append("")
                fy_row.append("")
                fz_row.append("")

        output_rows.append(fx_row)
        output_rows.append(fy_row)
        output_rows.append(fz_row)

    return output_rows


def write_csv(output_csv: Path, rows):
    with open(output_csv, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


def process_csv(input_csv: Path, output_csv: Path):
    rows = read_csv(input_csv)

    load_cases, node_data = extract_load_cases(rows)

    output_rows = build_output_rows(load_cases, node_data)

    write_csv(output_csv, output_rows)


def main():
    base_dir = Path(__file__).parent

    output_dir = base_dir / "Outputs"
    output_dir.mkdir(exist_ok=True)

    for input_csv in base_dir.glob("*.csv"):

        print(f"Processing: {input_csv.name}")

        output_csv = output_dir / f"{input_csv.stem}_output.csv"

        process_csv(input_csv, output_csv)

        print(f"Created: {output_csv.name}")

    print("Done.")


if __name__ == "__main__":
    main()

'''
Manikandan M
15 June 2026
'''
