from typing import Dict, Any

from pyniryo import NiryoRobot, PoseObject

from piecewalker.board_model import XYZ, get_board_point, list_to_xyz
from piecewalker.calibration.helper import parse_calibration_toml
from runtime.args import get_args_attr
from runtime.config import get_config

class Ned2:
    def build_pose_from_xyz(self, xyz: XYZ) -> PoseObject:
        gp = self.cfg["piecewalker"]["grasp_params"]
        roll = float(gp["roll"])
        pitch = float(gp["pitch"])
        yaw = float(gp["yaw"])

        return PoseObject(xyz.x, xyz.y, xyz.z, roll, pitch, yaw)

    def move(self, *, from_idx: int | None, to_idx: int | None) -> None:
        from_pose: PoseObject
        to_pose: PoseObject

        # Move From "unplaced_chips" Stack, if no from_idx was provided
        if from_idx is None:
            unplaced_chips_xyz: XYZ = list_to_xyz(self.calibration["points"]["unplaced_chips"])
            unplaced_chips_xyz.z = self._stack_z(unplaced_chips_xyz.z, self.unplaced_chips_count, for_pick=True)
            self.unplaced_chips_count -= 1
            from_pose = self.build_pose_from_xyz(unplaced_chips_xyz)

        # Move To "removed_chips" Stack, if no to_idx was provided
        if to_idx is None:
            removed_chips_xyz: XYZ = list_to_xyz(self.calibration["points"]["removed_chips"])
            removed_chips_xyz.z = self._stack_z(removed_chips_xyz.z, self.removed_chips_count, for_pick=False)
            self.removed_chips_count += 1
            to_pose = self.build_pose_from_xyz(removed_chips_xyz)

        # Move from/to concrete board position, if indicies were provided
        if from_idx is not None:
            from_xyz: XYZ = get_board_point(from_idx)
            from_pose = self.build_pose_from_xyz(from_xyz)
        if to_idx is not None:
            to_xyz: XYZ = get_board_point(to_idx)
            to_pose = self.build_pose_from_xyz(to_xyz)

        # Movement
        # Important, adjust z for the from and to pos, because they will be Stacks!
        self.robot.move(from_pose)
        self.robot.grasp_with_tool()

        self.robot.move(self._idle_pose)

        self.robot.move(to_pose)
        self.robot.release_with_tool()

        self.robot.move(self._idle_pose)

    def close(self) -> None:
        self.robot.close_connection()
        self.robot = None

    def _stack_z(self, base_z: float, count: int, *, for_pick: bool) -> float:
        """
        Returns the z-value adjusted for stack height.
        """
        chip_h = float(self.cfg["piecewalker"]["chip_height"])

        if count < 0:
            raise ValueError(f"stack count cannot be negative: {count}")

        if for_pick:
            return base_z + (count - 1) * chip_h
        else:
            return base_z + count * chip_h

    def _get_idle_pose(self) -> PoseObject:
        try:
            p = self.cfg["piecewalker"]["idle_pose"]
            return PoseObject(
                float(p["x"]), float(p["y"]), float(p["z"]),
                float(p["roll"]), float(p["pitch"]), float(p["yaw"])
            )
        except KeyError as e:
            raise ValueError(f"Missing config key for idle_pose in cfg file: {e}") from e

    def __init__(self) -> None:
        self.unplaced_chips_count = 9
        self.removed_chips_count = 0

        self.cfg = get_config()
        self.calibration_file_path: str | None = get_args_attr("calibration_file", None)
        self.calibration: Dict[str, Any] = parse_calibration_toml(self.calibration_file_path)

        # Connect robot
        ip = self.cfg["piecewalker"]["robot_ip"]
        self.robot = NiryoRobot(ip)
        self.robot.calibrate_auto()
        self.robot.update_tool()

        self._idle_pose = self._get_idle_pose()

    def __del__(self) -> None:
        # Fail-safe, don't rely on it, Python doesn't guarantee that __del__ will 100% be called.
        if self.robot is not None:
            self.robot.close_connection()
            