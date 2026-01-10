import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from pyniryo import NiryoRobot

from piecewalker.calibration.cli import parse_args
from runtime.config import get_config

from enum import Enum

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

def _record_xyz(robot: NiryoRobot, fixed_z_val: float | None) -> XYZ:
    """
    Returns the end effector pose for a particular calibration point.
    Documentation: https://niryorobotics.github.io/pyniryo/v1.2.1-1/examples/examples_movement.html#pose
    """
    pose = robot.get_pose()
    if fixed_z_val is None:
        return XYZ(pose.x, pose.y, pose.z)
    else:
        return XYZ(pose.x, pose.y, fixed_z_val)

def _build_toml_content(cli_args: argparse.Namespace, fixed_z_val: float | None, points: dict[CalibrationStep, XYZ]) -> str:
    # Build TOML text (simple, explicit)
    lines: list[str] = []
    lines.append("[general]")
    lines.append(f"used_fixed_z = {str(bool(cli_args.fixed_z)).lower()}")
    if fixed_z_val is not None:
        lines.append(f"fixed_z = {fixed_z_val}")
    lines.append("")

    lines.append("[points]")
    for step, p in points.items():
        # Use enum name as key
        key = step.name.lower()
        lines.append(f'{key} = [{p.x:.6f}, {p.y:.6f}, {p.z:.6f}]')

    lines.append("")
    return "\n".join(lines)

def _run_calibration(robot: NiryoRobot, cli_args: argparse.Namespace, config: Dict) -> str:
    points: dict[CalibrationStep, XYZ] = {}
    fixed_z_val: float | None = None
    if cli_args.fixed_z:
        fixed_z_val = float(config["piecewalker"]["fixed_z"])

    for step in CalibrationStep:
        input(f"Position robot to the: \"{step.value}\", then press Enter to record...")
        points[step] = _record_xyz(robot, fixed_z_val)

    return _build_toml_content(cli_args, fixed_z_val, points)

def _get_file_name(base_dir: Path, base_file_name: str) -> Path:
    """
    finds the first free index in the provided base_dir
    and then returns the adjusted file name
    """
    next_idx = 0
    while True:
        f = base_dir / f"{base_file_name}{next_idx:03d}.toml"
        if not f.exists():
            break
        next_idx += 1

    return base_dir / f"{base_file_name}{next_idx:03d}.toml"

def gen_calibration_file(robot: NiryoRobot, cli_args: argparse.Namespace, config: Dict) -> Path:
    """
    generates a new calibration file in the provided --path directory.
    """
    base_dir: Path = Path(cli_args.path).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    base_file_name = "calibration_"
    file_name = _get_file_name(base_dir, base_file_name)
    out_path = file_name

    content = _run_calibration(robot, cli_args, config)
    out_path.write_text(content, encoding="utf-8")
    return out_path

if __name__ == "__main__":
    args = parse_args()
    # CLI arguments are parsed as str but should be of type Path
    # Turn strings into absolute Paths
    path: Path = Path(args.path).resolve()

    cfg = get_config()

    # Robot should NOT be generated here, get it from somehwere...
    robot = NiryoRobot(cfg["piecewalker"]["robot_ip"])

    out_path = gen_calibration_file(robot, args, cfg)
    print("Wrote:", out_path)
