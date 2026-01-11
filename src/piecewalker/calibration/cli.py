import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrates the positions of the game board. "
                    "Creates a calibration_[idx].toml file inside of /configs/calibrations with a progressive index."
    )
    parser.add_argument(
        "--fixed_z",
        dest="fixed_z",
        action="store_true",
        help="If this flag is set, the z-value will not be based on the average of the calibration points. "
             "Instead, a hard-coded z-value will be used instead which has been defined in the \"niryo_config.toml\" file."
    )
    parser.set_defaults(fixed_z=False)
    return parser.parse_args()