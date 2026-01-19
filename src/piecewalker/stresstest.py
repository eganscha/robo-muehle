#!/usr/bin/env python3
"""
Ultra-minimal 9MM-ish stress test (exactly 20 calls to ned2.move)

Key constraint from your code:
- removed stack max height is 9, so we must do at most 9 moves with to_idx=None.

Assumptions / Setup:
- You manually place BLACK chips on the board BEFORE running this script.
- Robot places WHITE chips from its own stack (from_idx=None).
- After a scripted mill completion, we remove ONE black chip (to_idx=None).
- We remove ALL 9 black chips total (exactly 9 removals to removed stack).
- Final 2 moves are board -> board (do not affect removed stack height).

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
"""

from piecewalker import ned2_provider

if __name__ == "__main__":
    ned2 = ned2_provider.get_ned2()

    # ---- 20 moves total ----
    # 9x place white from stack -> board (exactly 9 picks from stack)
    # 9x remove black from board -> removed stack (exactly 9 removals, max safe)
    # 2x board -> board moves (extra coverage, no stack involved)

    # Mill 1 for white: 6-7-8
    ned2.move(from_idx=None, to_idx=6,  back_to_idle=False)     # 1  place W
    ned2.move(from_idx=None, to_idx=7,  back_to_idle=False)     # 2  place W
    ned2.move(from_idx=None, to_idx=8,  back_to_idle=False)     # 3  place W
    ned2.move(from_idx=0,    to_idx=None, back_to_idle=False)   # 4  remove B

    # Mill 2 for white: 18-19-20
    ned2.move(from_idx=None, to_idx=18, back_to_idle=False)     # 5  place W
    ned2.move(from_idx=None, to_idx=19, back_to_idle=False)     # 6  place W
    ned2.move(from_idx=None, to_idx=20, back_to_idle=False)     # 7  place W
    ned2.move(from_idx=2,    to_idx=None, back_to_idle=False)   # 8  remove B

    # Set up Mill 3 for white: 1-4-7 (7 already has W)
    ned2.move(from_idx=None, to_idx=1,  back_to_idle=False)     # 9  place W
    ned2.move(from_idx=None, to_idx=4,  back_to_idle=False)     # 10 place W -> completes mill (1,4,7)
    ned2.move(from_idx=3,    to_idx=None, back_to_idle=False)   # 11 remove B

    # Final (9th) white placement from stack
    ned2.move(from_idx=None, to_idx=14, back_to_idle=False)     # 12 place W (stack now empty)

    # Remove remaining black chips (6 more removals = total 9 removals)
    ned2.move(from_idx=5,    to_idx=None, back_to_idle=False)   # 13 remove B
    ned2.move(from_idx=10,   to_idx=None, back_to_idle=False)   # 14 remove B
    ned2.move(from_idx=12,   to_idx=None, back_to_idle=False)   # 15 remove B
    ned2.move(from_idx=16,   to_idx=None, back_to_idle=False)   # 16 remove B
    ned2.move(from_idx=22,   to_idx=None, back_to_idle=False)   # 17 remove B
    ned2.move(from_idx=23,   to_idx=None, back_to_idle=False)   # 18 remove B

    # Extra coverage without touching removed stack: board -> board moves
    # After removing all blacks, indices 0 and 23 are empty.
    ned2.move(from_idx=14,   to_idx=0,   back_to_idle=False)    # 19 move W: 14 -> 0
    ned2.move(from_idx=0,    to_idx=23,  back_to_idle=True)     # 20 move W: 0 -> 23 + idle

    ned2_provider.close_ned2()