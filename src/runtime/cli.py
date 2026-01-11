import argparse
from pathlib import Path

_ARGS: argparse.Namespace | None = None

def _parse_args():
    """parses the cli args for the runner subsystem"""
    parser = argparse.ArgumentParser(
        description=f"Runs the robo-muehle project. "
    )
    parser.add_argument(
        "--calibration_file",
        default=None,
        type=Path,
        help=f"Path if a particular calibration file should be used. Defaults to the calibration file with the highest index. "
    )

    return parser.parse_args()

def get_args():
    global _ARGS
    if _ARGS is not None:
        return _ARGS

    _ARGS = _parse_args()
    return _ARGS
