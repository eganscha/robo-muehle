import tomllib
from pathlib import Path
from typing import Dict, Any

from piecewalker.calibration.cli import get_configs_dir
from runtime.paths import build_paths

# Constants
CALIBRATION_FILE_PREFIX = "calibration_"
CALIBRATION_FILE_EXTENSION = ".toml"
CALIBRATION_INDEX_WIDTH = 3

def get_first_free_cfg_idx() -> int:
    """
    Returns the first available NEXT index for a calibration cfg file.
    """
    path = build_paths(configs_dir=get_configs_dir())

    next_idx = 0
    while True:
        f = path.calibrations_dir / f"{CALIBRATION_FILE_PREFIX}{next_idx:0{CALIBRATION_INDEX_WIDTH}}{CALIBRATION_FILE_EXTENSION}"
        if not f.exists():
            break
        next_idx += 1

    return next_idx

def _get_calibration_file_path(idx: int | None = None) -> Path | None:
    """
    returns the path to the calibration file
    :param idx: idx of the calibration file, if None is provided, latest will be returned
    :return: Path to the calibration file, or None if no calibration file was found
    """
    path = build_paths(configs_dir=get_configs_dir())

    if idx is None:
        # First free idx
        next_idx = get_first_free_cfg_idx()
        # Latest actually existing idx
        idx = next_idx - 1

    path = path.calibrations_dir / f"{CALIBRATION_FILE_PREFIX}{idx:0{CALIBRATION_INDEX_WIDTH}}{CALIBRATION_FILE_EXTENSION}"
    if path.is_file():
        return path
    else:
        return None

def parse_calibration_toml(idx: int | None = None) -> Dict[str, Any]:
    """
    returns the calibration config as a dictionary
    :param idx: idx of the calibration file, if None is provided, latest found will be returned
    :return: the calibration config as a dictionary
    """
    path = _get_calibration_file_path(idx=idx)
    if path is None or not path.is_file():
        raise FileNotFoundError(f"Calibration file not found at path: {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    general = data.get("general", {})
    points = data.get("points", {})
    file = {
        "path": path,
        "general": general,
        "points": points,
    }
    return file
