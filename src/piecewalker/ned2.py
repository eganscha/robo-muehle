from typing import Dict, Any

from pyniryo import NiryoRobot, PoseObject

from piecewalker.board_model import XYZ, get_board_point, list_to_xyz
from piecewalker.calibration.helper import parse_calibration_toml
from piecewalker.config import get_config
from runtime.args import parse_args

class Ned2:
    def build_pose_from_xyz(self, xyz: XYZ) -> PoseObject:
        gp = self.cfg["piecewalker"]["grasp_params"]
        roll = float(gp["roll"])
        pitch = float(gp["pitch"])
        yaw = float(gp["yaw"])

        return PoseObject(xyz.x, xyz.y, xyz.z, roll, pitch, yaw)

    def _pick_z(self, z: float) -> float:
        return z + float(self.cfg["piecewalker"].get("pick_z_offset", 0.0))

    def _place_z(self, z: float) -> float:
        return z + float(self.cfg["piecewalker"].get("place_z_offset", 0.0))

    def move(self, *, from_idx: int | None, to_idx: int | None) -> None:
        from_pose: PoseObject
        to_pose: PoseObject

        # Move From "unplaced_chips" Stack, if no from_idx was provided
        if from_idx is None:
            unplaced_chips_xyz: XYZ = list_to_xyz(self.calibration["points"]["unplaced_chips"])
            unplaced_chips_xyz.z = self._stack_z(unplaced_chips_xyz.z, self.unplaced_chips_count, for_pick=True)
            self.unplaced_chips_count -= 1
            from_pose = self.build_pose_from_xyz(unplaced_chips_xyz)
        else:
            # Move to concrete board position, if from_idx was provided
            from_xyz: XYZ = get_board_point(from_idx)
            from_pose = self.build_pose_from_xyz(from_xyz)

        # Move To "removed_chips" Stack, if no to_idx was provided
        if to_idx is None:
            removed_chips_xyz: XYZ = list_to_xyz(self.calibration["points"]["removed_chips"])
            removed_chips_xyz.z = self._stack_z(removed_chips_xyz.z, self.removed_chips_count, for_pick=False)
            self.removed_chips_count += 1
            to_pose = self.build_pose_from_xyz(removed_chips_xyz)
        else:
            # Move to concrete board position, if to_idx was provided
            to_xyz: XYZ = get_board_point(to_idx)
            to_pose = self.build_pose_from_xyz(to_xyz)

        # Movement
        print("\nMoving into idle pose:\n", self._idle_pose)
        self.robot.move_pose(self._idle_pose)
        self.robot.release_with_tool()

        print("\nfrom_pose:\n", from_pose)
        print("\nto_pose:\n", to_pose)

        # ---------- PICK ----------
        # go above pick position (same x/y as from_pose, safe z = idle z)
        from_above = PoseObject(
            from_pose.x, from_pose.y, self._idle_pose.z,
            from_pose.roll, from_pose.pitch, from_pose.yaw
        )
        print("\nMoving above pick position (from_above):\n", from_above)
        self.robot.move_pose(from_above)

        # descend to pick
        # descend to pick (use small offset)
        pick_pose = PoseObject(from_pose.x, from_pose.y, self._pick_z(from_pose.z),
                               from_pose.roll, from_pose.pitch, from_pose.yaw)
        print("\nDescending to pick (pick_pose):\n", pick_pose)
        self.robot.move_pose(pick_pose)
        self.robot.grasp_with_tool()

        # retreat up before traveling
        print("\nRetreating up (from_above):\n", from_above)
        self.robot.move_pose(from_above)

        # ---------- PLACE ----------
        # go above place position
        to_above = PoseObject(
            to_pose.x, to_pose.y, self._idle_pose.z,
            to_pose.roll, to_pose.pitch, to_pose.yaw
        )
        print("\nMoving above place position (to_above):\n", to_above)
        self.robot.move_pose(to_above)

        # descend to place (use small offset)
        place_pose = PoseObject(to_pose.x, to_pose.y, self._place_z(to_pose.z),
                                to_pose.roll, to_pose.pitch, to_pose.yaw)
        print("\nDescending to place (place_pose):\n", place_pose)
        self.robot.move_pose(place_pose)
        self.robot.release_with_tool()

        # retreat up then back to idle
        print("\nRetreating up (to_above):\n", to_above)
        self.robot.move_pose(to_above)

        print("\nBack to idle pose:\n", self._idle_pose)
        self.robot.move_pose(self._idle_pose)

    def close(self) -> None:
        self.robot.close_connection()
        self.robot = None

    def _stack_z(self, base_z: float, count: int, for_pick: bool) -> float:
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
        print("Initializing Ned2 instance...")
        self.unplaced_chips_count = 9
        self.removed_chips_count = 0

        self.cfg = get_config()
        self.args = parse_args()
        self.calibration_file_path: str | None = self.args.get("calibration_file_path", None)
        self.calibration: Dict[str, Any] = parse_calibration_toml(self.calibration_file_path)

        # Connect robot
        ip = self.cfg["piecewalker"]["robot_ip"]
        print("Connecting to robot...")
        self.robot = NiryoRobot(ip)
        print("Calibrating and updating tool...")
        self.robot.calibrate_auto()
        self.robot.update_tool()

        self._idle_pose = self._get_idle_pose()
        print("Moving into idle pose...")
        self.robot.move_pose(self._idle_pose)

    def __del__(self) -> None:
        # Fail-safe, don't rely on it, Python doesn't guarantee that __del__ will 100% be called.
        if self.robot is not None:
            self.robot.close_connection()
