import argparse

DEFAULT_CONFIG_PATH: str = "configs"
DEFAULT_CALIBRATIONS_PATH: str = f"{DEFAULT_CONFIG_PATH}/calibrations"

def parse_args():
    """parses the cli args for the piecewalkers calibration subsystem"""
    parser = argparse.ArgumentParser(
        description=f"Calibrates the positions of the game board. "
                    f"Creates a calibration_[idx].toml file inside of /configs/calibrations with a progressive index."
    )
    parser.add_argument(
        "--path",
        default=str(DEFAULT_CALIBRATIONS_PATH),
        type=str,
        help=   f"Path where the calibration_[idx].toml file is stored. "
                f"If none is provided, \"{DEFAULT_CALIBRATIONS_PATH}\" will be used.",
    )
    parser.add_argument(
        "--fixed_z",
        dest="fixed_z",
        action="store_true",
        help=   f"Do not calculate the z-value based off of the average of the calibration points. "
                f"Instead, use a hard-coded z-value that will work for your particular board defined inside the "
                f"\"{DEFAULT_CALIBRATIONS_PATH}/niryo_config.toml\" file.",
    )
    parser.set_defaults(fixed_z=False)

    return parser.parse_args()
