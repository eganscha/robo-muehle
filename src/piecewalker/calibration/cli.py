import argparse
from argparse import Namespace

_ARGS: Namespace | None = None

def _parse_args():
    """parses the cli args for the piecewalkers calibration subsystem"""
    parser = argparse.ArgumentParser(
        description=f"Calibrates the positions of the game board. "
                    f"Creates a calibration_[idx].toml file inside of /configs/calibrations with a progressive index."
    )
    parser.add_argument(
        "--fixed_z",
        dest="fixed_z",
        action="store_true",
        help=f"If this flag is set, the z-value will not be based on the average of the calibration points. "
             f"Instead, a hard-coded z-value will be used instead which has been defined in the \"niryo_config.toml\" file."
    )
    parser.set_defaults(fixed_z=False)

    return parser.parse_args()

def get_args():
    global _ARGS
    if _ARGS is not None:
        return _ARGS

    _ARGS = _parse_args()
    return _ARGS
