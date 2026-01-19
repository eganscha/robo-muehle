#!/usr/bin/env python3
"""
Reduced stress test: ONLY collect black chips from the board into the removed stack.

Setup:
- Manually place 9 BLACK chips on the board at the indices listed in BLACK_START.
- Ensure removed stack is empty before you start (removed_chips_count starts at 0 on init).
- This script performs exactly 9 moves: board[idx] -> removed stack (to_idx=None).

Manual BLACK placement (9 chips, no initial mill; wide spread):
BLACK_START = [0, 2, 3, 5, 10, 12, 16, 22, 23]

Graphic (B = place BLACK chip here):

  0(B) ---------------------- 1 --------------------- 2(B)
   |                        |                       |
   |                        |                       |
   |         3(B) --------- 4 ----------- 5(B)       |
   |         |              |             |         |
   |         |              |             |         |
   |         |      6 ----- 7 ----- 8     |         |
   |         |      |               |     |         |
   |         |      |               |     |         |
  9 ------  10(B) --11             12(B) --13 ----- 14
   |         |      |               |     |         |
   |         |      |               |     |         |
   |         |      15 ---- 16(B) --17     |         |
   |         |              |             |         |
   |         |              |             |         |
   |         18 ----------- 19 ---------- 20        |
   |                        |                       |
   |                        |                       |
  21 --------------------- 22(B) ------------------- 23(B)

Notes:
- Removed stack has a hard max of 9 in your Ned2.move() implementation.
"""

from piecewalker import ned2_provider

BLACK_START = [0, 2, 3, 5, 10, 12, 16, 22, 23]

if __name__ == "__main__":
    ned2 = ned2_provider.get_ned2()

    # Collect all black chips into removed stack.
    # back_to_idle=True on the last move only.
    for i, idx in enumerate(BLACK_START):
        back_to_idle = (i == len(BLACK_START) - 1)
        ned2.move(from_idx=idx, to_idx=None, back_to_idle=back_to_idle)

    ned2_provider.close_ned2()