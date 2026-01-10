from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from piecewalker.calibration.cli import get_args, get_configs_dir
from piecewalker.calibration.helper import CALIBRATION_FILE_PREFIX, CALIBRATION_INDEX_WIDTH, CALIBRATION_FILE_EXTENSION
from piecewalker.calibration.helper import get_first_free_cfg_idx
# from piecewalker.core import get_robot
from piecewalker.mock_core import get_robot
from runtime.config import get_config
from runtime.paths import build_paths


class CalibrationStep(Enum):
    CORNER_A = "Corner A (origin)"
    CORNER_B = "Corner B (width)"
    CORNER_C = "Corner C (height)"
    UNPLACED_CHIPS = "Unplaced Chips Stack"
    REMOVED_CHIPS = "Removed Chips Stack"

@dataclass(frozen=True)
class XYZ:
    x: float
    y: float
    z: float

def _record_xyz() -> XYZ:
    """
    Returns the end effector pose for a particular calibration point.
    Documentation: https://niryorobotics.github.io/pyniryo/v1.2.1-1/examples/examples_movement.html#pose
    """
    robot = get_robot()
    args = get_args()
    cfg = get_config()

    fixed_z_val: float | None = None
    if args.fixed_z:
        fixed_z_val = float(cfg["piecewalker"]["fixed_z"])

    pose = robot.get_pose()
    if fixed_z_val is None:
        return XYZ(pose.x, pose.y, pose.z)
    else:
        return XYZ(pose.x, pose.y, fixed_z_val)


# noinspection PyListCreation
def _build_toml_content(points: dict[CalibrationStep, XYZ]) -> str:
    lines: list[str] = []
    lines.append("[general]")
    lines.append("")

    lines.append("[points]")
    for step, p in points.items():
        # Use enum name as key
        key = step.name.lower()
        lines.append(f'{key} = [{p.x:.6f}, {p.y:.6f}, {p.z:.6f}]')

    lines.append("")
    return "\n".join(lines)

def _run_calibration() -> str:
    points: dict[CalibrationStep, XYZ] = {}
    for step in CalibrationStep:
        input(f"Position robot to the: \"{step.value}\", then press Enter to record...")
        points[step] = _record_xyz()

    return _build_toml_content(points)

def _get_next_file_name() -> Path:
    """
    finds the first free index in the calibrations dir
    and then returns the file name as a Path object
    """
    next_idx = get_first_free_cfg_idx()
    file_name = Path(f"{CALIBRATION_FILE_PREFIX}{next_idx:0{CALIBRATION_INDEX_WIDTH}}{CALIBRATION_FILE_EXTENSION}")

    return file_name

def _gen_calibration_file() -> Path:
    """
    generates a new calibration file in the provided --path directory.
    """
    path = build_paths(configs_dir=get_configs_dir())
    path.calibrations_dir.mkdir(parents=True, exist_ok=True)

    file_name = _get_next_file_name()
    target_path = path.calibrations_dir / file_name

    content = _run_calibration()
    target_path.write_text(content, encoding="utf-8")
    return target_path

if __name__ == "__main__":
    out_path = _gen_calibration_file()
    print("Wrote:", out_path)
