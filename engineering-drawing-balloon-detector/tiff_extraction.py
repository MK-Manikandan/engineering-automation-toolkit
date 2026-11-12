import time
start = time.perf_counter()

import pytesseract
# Point this to your standard Tesseract path just in case the system doesn't have tesserocr
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mmohandas\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

import argparse
import csv
import os
import sys
import cv2
import concurrent.futures
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from balloon_lib import (load_ink_mask, detect_balloons, compute_leader_line_groups,
                          detect_grid_zones, grid_zone_label)

Image.MAX_IMAGE_PIXELS = None


def annotate_image(ink, balloons, line_color=(0, 0, 255), line_thickness=None,
                    label=True, label_color=(255, 0, 0)):
    h, w = ink.shape
    vis = cv2.cvtColor(255 - ink, cv2.COLOR_GRAY2BGR)
    if line_thickness is None:
        line_thickness = max(2, int(round(min(h, w) / 1400)))
    font_scale = max(0.8, min(h, w) / 2800)
    font_thickness = max(2, line_thickness - 1)
    for b in balloons:
        try:
            cx, cy, r = int(round(b['cx'])), int(round(b['cy'])), int(round(b['radius']))
        except (KeyError, TypeError, ValueError):
            continue  
        cv2.circle(vis, (cx, cy), r, line_color, line_thickness)
        if label:
            text = str(b.get('text', '?'))
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            tx = cx - tw // 2
            ty = cy - r - int(0.25 * r) - 4
            ty = max(ty, th + 2)
            cv2.rectangle(vis, (tx - 3, ty - th - 3), (tx + tw + 3, ty + 3), (255, 255, 255), -1)
            cv2.putText(vis, text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, label_color, font_thickness, cv2.LINE_AA)
    return vis


def write_report(balloons, csv_path, source_name, col_centers=None, row_centers=None):
    col_centers = col_centers or {}
    row_centers = row_centers or {}
    balloons_sorted = sorted(
        balloons,
        key=lambda b: (round(b.get('cy', 0) / 50), b.get('cx', 0)))
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['source_file', 'balloon_number', 'grid_zone', 'radius_px'])
        for b in balloons_sorted:
            try:
                zone = grid_zone_label(b['cx'], b['cy'], col_centers, row_centers)
                writer.writerow([source_name, b.get('text', '?'), zone, int(round(b['radius']))])
            except (KeyError, TypeError, ValueError):
                continue


def append_leader_line_report(leader_groups, csv_path, blank_lines=3):
    if not leader_groups: return
    try:
        with open(csv_path, 'a', newline='') as f:
            for _ in range(blank_lines): f.write('\r\n')
            writer = csv.writer(f)
            for g in leader_groups:
                texts = g.get('balloon_texts') or []
                if not texts: continue
                label = '-'.join(str(t) for t in texts)
                writer.writerow(["'" + label, g.get('leader_count', 0)])
    except OSError as e:
        print(f"  !! Could not append leader-line section to {csv_path}: {e}")


def process_file(in_path, out_dir, verbose=True):
    """Processes a single file. Captures logs to print as a block to avoid multiprocessing console mess."""
    logs = []
    base = os.path.splitext(os.path.basename(in_path))[0]

    def progress(msg):
        if verbose: logs.append(f"  [{base}] {msg}")

    t0 = time.time()
    logs.append(f"Processing {os.path.basename(in_path)} ...")
    
    try:
        ink, pil_img = load_ink_mask(in_path)
        logs.append(f"  [{base}] image size: {ink.shape[1]}x{ink.shape[0]} px")
        
        balloons = detect_balloons(ink, progress=progress)

        try:
            col_centers, row_centers = detect_grid_zones(ink, progress=progress)
        except Exception as e:
            logs.append(f"  !! Grid zone detection failed for {in_path} ({e}); grid_zone column will be blank.")
            col_centers, row_centers = {}, {}

        vis = annotate_image(ink, balloons)
        out_img_path = os.path.join(out_dir, f"{base}_balloons_marked.png")
        if not cv2.imwrite(out_img_path, vis):
            raise IOError(f"Failed to write annotated image to {out_img_path}")

        out_csv_path = os.path.join(out_dir, f"{base}_balloons_report.csv")
        write_report(balloons, out_csv_path, os.path.basename(in_path), col_centers, row_centers)

        try:
            leader_groups = compute_leader_line_groups(ink, balloons, progress=progress)
            append_leader_line_report(leader_groups, out_csv_path)
            n_leader_lines = sum(g.get('leader_count', 0) for g in leader_groups)
            progress(f"Leader-line groups written: {len(leader_groups)} (total leader lines counted: {n_leader_lines})")
        except Exception as e:
            logs.append(f"  !! Leader-line counting failed for {in_path} ({e}); section skipped.")

        dt = time.time() - t0
        if balloons:
            numbers = sorted((b.get('text', '?') for b in balloons), key=lambda s: (len(s), s))
            logs.append(f"  -> {len(balloons)} balloons found in {dt:.1f}s: {', '.join(numbers)}")
        else:
            logs.append(f"  -> 0 balloons found in {dt:.1f}s")
            
        logs.append(f"  -> annotated image: {out_img_path}")
        logs.append(f"  -> report: {out_csv_path}")
        
    except Exception as general_err:
        logs.append(f"  !! FAILED on {in_path}: {general_err}")
        print("\n".join(logs))
        raise general_err
        
    # Flush logs securely at the end of the process
    print("\n".join(logs))
    return out_img_path, out_csv_path, balloons


def main():
    ap = argparse.ArgumentParser(description="Detect number-in-circle balloons in engineering drawing TIFFs.")
    ap.add_argument('inputs', nargs='*', help="Input TIFF file(s)")
    ap.add_argument('--input-dir', help="Process every .tif/.tiff file in this directory")
    ap.add_argument('-o', '--output-dir', default='/mnt/user-data/outputs', help="Directory to write annotated images and CSV reports")
    args = ap.parse_args()

    files = list(args.inputs)
    if args.input_dir:
        if not os.path.isdir(args.input_dir):
            ap.error(f"--input-dir '{args.input_dir}' is not a directory.")
        try:
            entries = sorted(os.listdir(args.input_dir))
            for fn in entries:
                if fn.lower().endswith(('.tif', '.tiff')):
                    files.append(os.path.join(args.input_dir, fn))
        except OSError as e:
            ap.error(f"Could not list --input-dir '{args.input_dir}': {e}")

    if not files: ap.error("No input files given.")

    missing = [f for f in files if not os.path.isfile(f)]
    if missing: ap.error("File(s) not found: " + ", ".join(missing))

    try: os.makedirs(args.output_dir, exist_ok=True)
    except OSError as e: ap.error(f"Could not create --output-dir '{args.output_dir}': {e}")
    if not os.access(args.output_dir, os.W_OK): ap.error(f"--output-dir '{args.output_dir}' is not writable.")

    # Execute utilizing Process Pool (multi-core architecture)
    max_workers = min(os.cpu_count() or 1, len(files))
    print(f"Launching File Processing across {max_workers} CPU cores...\n")
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, f, args.output_dir): f for f in files}
        for future in concurrent.futures.as_completed(futures):
            f = futures[future]
            try:
                future.result()
            except Exception as e:
                # Top level failure already logged by the process_file func
                pass

if __name__ == '__main__':
    # Required for Windows multiprocessing compatibility
    import multiprocessing
    multiprocessing.freeze_support()
    main()
    
    end = time.perf_counter()
    print(f"\nTotal Execution time: {end - start:.6f} seconds")

'''
Manikandan M
'''
