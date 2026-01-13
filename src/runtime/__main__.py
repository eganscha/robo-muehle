from piecewalker.ned2 import Ned2
from piecewalker.ned2_provider import get_ned2, close_ned2

if __name__ == "__main__":
    ned2: Ned2 = get_ned2()

    ned2.move(from_idx=None, to_idx=3)
    ned2.move(from_idx=3, to_idx=1)
    ned2.move(from_idx=16, to_idx=None)

    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)
    # ned2.move(from_idx=None, to_idx=None)

    close_ned2()