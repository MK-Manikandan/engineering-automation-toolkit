# Engineering Drawing Balloon Detector

Apart from the pip packages, it requires manual installation of `pytesseract` from:
`https://github.com/UB-Mannheim/tesseract/wiki`

Finds **"balloons"** (numbers enclosed in circles, connected to parts via leader
lines) in scanned engineering drawing TIFF files, and produces:

1. An annotated copy of the drawing with every detected balloon circled
   and labeled.
2. A CSV report of every detected balloon containing:
   - Balloon number
   - Pixel location
   - Radius

## Usage

```bash
python3 detect_balloons_main.py INPUT.tif [INPUT2.tif ...] -o OUTPUT_DIR
python3 detect_balloons_main.py --input-dir DIR -o OUTPUT_DIR
```

## Design Notes

### Why this approach?

- Balloons are circles with leader lines touching them, which means a
  naive **"connected component must be a clean circle"** approach fails.
  The leader line merges the circle into a much larger, irregularly-shaped
  ink blob.

- Instead, the algorithm looks at the **hole inside the ring**
  (the background region enclosed by the ring's ink) using
  **contour hierarchy analysis**.

- The hole's own boundary remains a clean circle regardless of what
  touches the balloon from the outside, making the detection method
  significantly more robust.

### Automatic Size Calibration

- Different drawings and scans use very different pixel scales.
- The expected balloon size is automatically calibrated for each drawing
  by searching for a natural gap in the candidate-hole size histogram.

### OCR Validation

- Every candidate must successfully OCR as a **pure digit string**.
- This rejects:
  - Round letters such as `O`, `D`, and `Q`
  - Ground symbols
  - ESD symbols
  - Hex-bolt circles
  - Hole callouts
  - Other circular objects without numeric labels

### Recovery of Dashed or Broken Balloons

- Dashed or broken circles often used for alternate or reference parts
  do not create a clean contour hole.
- A secondary **Hough Circle Transform** sweep is used to recover these.
- Candidates are accepted only if they satisfy:
  - Ring completeness checks
  - OCR digit validation

### False Positive Reduction

- A small bottom-right exclusion region is applied.
- This reduces false positives originating from:
  - Handwritten signatures
  - Approval stamps
  - Title block markings

These regions can occasionally resemble circled digits to a generic
detector and are therefore ignored.
