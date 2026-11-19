"""Recalculate top-label calibration error from exported predictions."""

import argparse
import csv
import sys
from fractions import Fraction
from math import ceil
from pathlib import Path

BIN_COUNT = 15
EXAMPLE = Path(__file__).parent / "examples" / "six-predictions.csv"


def bin_predictions(source):
    reader = csv.reader(source, strict=True)
    if next(reader, None) != ["confidence", "correct"]:
        raise ValueError("expected CSV header confidence,correct")
    counts = [0] * BIN_COUNT
    correct = [0] * BIN_COUNT
    confidence_sums = [Fraction(0) for _ in range(BIN_COUNT)]
    for row in reader:
        if len(row) != 2 or row[1] not in ("0", "1"):
            raise ValueError(f"line {reader.line_num}: expected confidence and 0 or 1")
        try:
            confidence = Fraction(row[0])
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"line {reader.line_num}: invalid confidence") from exc
        if not 0 <= confidence <= 1:
            raise ValueError(f"line {reader.line_num}: confidence outside [0, 1]")
        index = max(0, ceil(confidence * BIN_COUNT) - 1)
        counts[index] += 1
        correct[index] += int(row[1])
        confidence_sums[index] += confidence
    if not any(counts):
        raise ValueError("input has no predictions")
    return list(zip(counts, correct, confidence_sums))


def calibration_errors(bins):
    total = sum(count for count, _, _ in bins)
    gaps = [correct - confidence for _, correct, confidence in bins]
    return sum(map(abs, gaps)) / total, abs(sum(gaps)) / total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", nargs="?", type=Path, default=EXAMPLE)
    args = parser.parse_args()
    try:
        with args.predictions.open(encoding="utf-8", newline="") as source:
            bins = bin_predictions(source)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"{args.predictions}: {exc}\n")

    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["bin", "count", "correct", "confidence_sum"])
    for number, (count, correct, confidence) in enumerate(bins, start=1):
        writer.writerow([number, count, correct, str(confidence)])
    ece, pooled = calibration_errors(bins)
    print(f"15-bin ECE: {float(ece):.2%}", file=sys.stderr)
    print(f"Pooled gap: {float(pooled):.2%}", file=sys.stderr)


if __name__ == "__main__":
    main()
