from pyniryo import NiryoRobot

from piecewalker.calibration.helper import parse_calibration_toml
# from piecewalker.core import get_robot
from piecewalker.mock_core import get_robot
from runtime.config import get_config

class Ned2:
    def __init__(self):
        self.robot: NiryoRobot = get_robot()
        if self.robot is None:
            raise RuntimeError(f"Could not initialize Ned2, no NiryoRobot found.")

        self.cfg = get_config()
        self.calib_toml = parse_calibration_toml()

    # Python's stupid, doesn't guarantee this will be called. Use a .close function and just call it as a failsafe here instead.
    def __del__(self):
        if self.robot is not None:
            print("Closing NiryoNed2 connection...")
            self.robot.close_connection()
        else:
            assert "Could not close NiryoNed2 connection, no NiryoRobot found."