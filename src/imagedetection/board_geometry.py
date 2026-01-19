import csv
from pathlib import Path

BOARD_SIZE = 1000  # in px

class BoardIndexMap:
    def __init__(self, csv_path):
        self.indices = {}
        self._load(csv_path)

    def _load(self, csv_path):
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.indices[int(row["index_id"])] = (
                    float(row["x_rel"]),
                    float(row["y_rel"])
                )

    def rel_to_abs(self, x_rel, y_rel):
        return (
            x_rel * BOARD_SIZE,
            y_rel * BOARD_SIZE
        )

    def get_abs_indices(self):
        return {
            idx: self.rel_to_abs(x, y)
            for idx, (x, y) in self.indices.items()
        }