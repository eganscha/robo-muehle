from pyniryo import PoseObject, NiryoRobot

from runtime.config import get_config

_ROBOT: NiryoRobot | None = None

def get_robot() -> NiryoRobot:
    global _ROBOT
    if _ROBOT is not None:
        return _ROBOT

    config = get_config()
    ip = config["piecewalker"]["robot_ip"]

    robot = NiryoRobot(ip)
    robot.calibrate_auto()
    robot.update_tool()

    _ROBOT = robot
    return _ROBOT

def get_idle_pose() -> PoseObject:
    config = get_config()
    try:
        p = config["piecewalker"]["idle_pose"]
        return PoseObject(
            float(p["x"]), float(p["y"]), float(p["z"]),
            float(p["roll"]), float(p["pitch"]), float(p["yaw"])
        )
    except KeyError as e:
        raise ValueError(f"Missing config key for idle_pose: {e}") from e