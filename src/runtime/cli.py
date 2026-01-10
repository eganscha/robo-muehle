import argparse
from pathlib import Path

from runtime.paths import DEFAULT_CONFIGS_DIR

_ARGS: argparse.Namespace | None = None

def _parse_args():
    """parses the cli args for the runner subsystem"""
    parser = argparse.ArgumentParser(
        description=f"Runs the robo-muehle project. "
    )
    parser.add_argument(
        "--configs_dir",
        default=str(f"{DEFAULT_CONFIGS_DIR}"),
        type=str,
        help=f"Path to the configs directory. Defaults to {DEFAULT_CONFIGS_DIR}. "
    )

    return parser.parse_args()

def get_args():
    global _ARGS
    if _ARGS is not None:
        return _ARGS

    _ARGS = _parse_args()
    return _ARGS

def get_configs_dir() -> Path:
    args = get_args()
    return Path(args.configs_dir).resolve()