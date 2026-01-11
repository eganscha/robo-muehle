from pyniryo import NiryoRobot

from piecewalker.calibration.helper import parse_calibration_toml
# from piecewalker.core import get_robot
from piecewalker.mock_core import get_robot
from runtime.cli import get_args
from runtime.config import get_config

class Ned2:
    def __init__(self):
        self.robot: NiryoRobot = get_robot()
        if self.robot is None:
            raise RuntimeError(f"Could not initialize Ned2, no NiryoRobot found.")

        self.cfg = get_config()
        self.args = get_args()
        self.calib_toml = parse_calibration_toml(self.args.calibration_file)
        print(self.calib_toml)

    # 1. Python's stupid, doesn't guarantee this will be called. Use a .close function and just call it as a failsafe here instead.
    # 2. Merge core into ned2.py
    # 3. Calculate based off of the calibration the points of the field
    # 4. Provide basic implementation for movement, maybe move_to, or some shit ...
    # 5. In General, think about what Frederik needs and then implement that function
    
    def __del__(self):
        if self.robot is not None:
            print("Closing NiryoNed2 connection...")
            self.robot.close_connection()
        else:
            assert "Could not close NiryoNed2 connection, no NiryoRobot found."