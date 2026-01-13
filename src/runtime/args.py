import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Runs the robo-muehle project.")
    parser.add_argument(
        "--calibration_file",
        default=None,
        type=Path,
        help="Path if a particular calibration file should be used. Defaults to the calibration file with the highest index.",
    )
    parser.add_argument(
        "--model-play",
        default=None,
        type=Path,
    )
    return parser.parse_args()
