from unittest.mock import Mock
from types import SimpleNamespace
from pyniryo import PoseObject
from runtime.config import get_config

_ROBOT = None

def get_robot():
    global _ROBOT
    if _ROBOT is not None:
        return _ROBOT

    robot = Mock(name="MockNiryoRobot")
    robot.calibrate_auto.return_value = None
    robot.update_tool.return_value = None

    robot.get_pose.return_value = SimpleNamespace(
        x=0.20, y=0.10, z=0.34, roll=0.0, pitch=0.0, yaw=0.0
    )
    robot.move.return_value = None
    _ROBOT = robot
    return _ROBOT

def get_idle_pose() -> PoseObject:
    cfg = get_config()
    p = cfg["piecewalker"]["idle_pose"]
    return PoseObject(float(p["x"]), float(p["y"]), float(p["z"]),
                      float(p["roll"]), float(p["pitch"]), float(p["yaw"]))
