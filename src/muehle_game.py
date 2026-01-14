from enum import Enum
from typing import Literal, cast

import numpy as np


class Phase(Enum):
    PLACING = 0
    MOVING = 1
    JUMPING = 2


class Muehle:
    board: np.ndarray
    to_place: dict[int, int]
    "valid moves if empty"
    vm: dict[int, list[int]]
    mills: list[list[int]]
    player: Literal[1, -1]

    """Nur klassenbasiert für dich Eugen"""

    def __init__(self):
        self.vm = self._make_vm()
        self.mills = self._make_mills()
        self.reset(reinit_board=True)

    def _is_jumping(self, player: Literal[1, -1]) -> bool:
        return (self.board == player).sum() == 3 and self._is_moving(player)

    def _is_moving(self, player: Literal[1, -1]) -> bool:
        return self.to_place[player] == 0

    def _has_lost(self, player: Literal[1, -1]) -> bool:
        if self._is_moving(player) and (self.board == player).sum() < 3:
            return True
        if self.phase(player) == Phase.MOVING:
            legal_mask = self.legal_actions_mask()
            if not legal_mask.any():
                return True
        return False

    def _truce(self):
        return self._is_jumping(1) and self._is_jumping(-1)

    def done(self):
        """
        returns the id of the winner or 0 for ongoing game
        """
        if self._has_lost(1):
            return -1
        if self._has_lost(-1):
            return 1
        return 0

    def is_terminal(self):
        return self.done() != 0 or self._truce()

    def phase(self, player: Literal[1, -1]) -> Phase:
        if not self._is_moving(player):
            return Phase.PLACING
        elif not self._is_jumping(player):
            return Phase.MOVING
        else:
            return Phase.JUMPING

    def reset(self, reinit_board=False):
        if reinit_board:
            self.board = np.zeros(24, dtype=np.int8)
        else:
            self.board[:] = 0
        self.to_place = {1: 9, -1: 9}
        self.player = 1

    def legal_actions_mask(self):
        mask = np.zeros(24, dtype=bool)
        p = self.player
        ph = self.phase(p)

        if ph == Phase.PLACING:
            mask[self.board == 0] = True
        elif ph == Phase.MOVING:
            for i in range(24):
                if self.board[i] == p:
                    for target in self.vm[i]:
                        if self.board[target] == 0:
                            mask[target] = True
        elif ph == Phase.JUMPING:
            for i in range(24):
                if self.board[i] == 0:
                    mask[i] = True
        return mask

    def move(self, source: int | None, target: int):
        p = self.player
        ph = self.phase(p)

        if ph == Phase.PLACING:
            if self.board[target] != 0:
                raise ValueError("Invalid move")
            self.board[target] = p
            self.to_place[p] -= 1
            if self.is_mill(target, p):
                return "remove"
        else:
            if source is None:
                raise ValueError("Invalid source")
            if self.board[source] != p:
                raise ValueError("Invalid source")
            if ph == Phase.MOVING and target not in self.vm[source]:
                raise ValueError("Invalid target")
            if self.board[target] != 0:
                raise ValueError("Invalid target")

            self.board[source] = 0
            self.board[target] = p
            if self.is_mill(target, p):
                return "remove"

        if self.done() != 0:
            return "done"
        self.player = cast(Literal[-1, 1], self.player * -1)
        return "ok"

    def remove_piece(self, pos: int):
        """
        Returns the winner or 0 for ongoing game
        """
        if not self.can_remove(pos, self.player):
            raise ValueError("Cannot remove piece from mill")
        # inverse because toggle happens on move and moves sends the signal that it can remove a field
        if self.board[pos] != self.player:
            raise ValueError("Can only remove opponent piece")
        self.board[pos] = 0
        return self.done()

    def is_mill(self, pos: int, player: Literal[1, -1]) -> bool:
        for mill in self.mills:
            if pos in mill and all(self.board[p] == player for p in mill):
                return True
        return False

    def _make_mills(self):
        return [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
            [12, 13, 14],
            [15, 16, 17],
            [18, 19, 20],
            [21, 22, 23],
            [0, 9, 21],
            [3, 10, 18],
            [6, 11, 15],
            [1, 4, 7],
            [16, 19, 22],
            [8, 12, 17],
            [5, 13, 20],
            [2, 14, 23],
        ]

    def can_remove(self, pos: int, remover: Literal[1, -1]) -> bool:
        """Check if opponent piece at pos can be removed."""
        if self.board[pos] != -remover:
            return False

        opponent = -remover
        opponent_pieces = [i for i in range(24) if self.board[i] == opponent]

        # Find pieces NOT in mills
        non_mill_pieces = [p for p in opponent_pieces if not self.is_mill(p, opponent)]

        # If there are non-mill pieces, can only remove those
        if non_mill_pieces:
            return pos in non_mill_pieces
        # All pieces in mills - can remove any
        return True

    def _make_vm(self):
        # It took longer to create the graphic than writing the code
        # 0 ---------------------- 1 --------------------- 2
        # |                        |                       |
        # |                        |                       |
        # |         3 ------------ 4 ----------- 5         |
        # |         |              |             |         |
        # |         |              |             |         |
        # |         |      6 ----- 7 ----- 8     |         |
        # |         |      |               |     |         |
        # |         |      |               |     |         |
        # 9 ------  10 --- 11             12 --- 13 ----- 14
        # |         |      |               |     |         |
        # |         |      |               |     |         |
        # |         |      15 ---- 16 ----17     |         |
        # |         |              |             |         |
        # |         |              |             |         |
        # |         18 ----------- 19 ---------- 20        |
        # |                        |                       |
        # |                        |                       |
        # 21 --------------------- 22 -------------------- 23

        return {
            0: [1, 9],
            1: [0, 2, 4],
            2: [1, 14],
            3: [4, 10],
            4: [1, 3, 5, 7],
            5: [4, 13],
            6: [7, 11],
            7: [4, 6, 8],
            8: [7, 12],
            9: [0, 10, 21],
            10: [3, 9, 11, 18],
            11: [6, 10, 15],
            12: [8, 13, 17],
            13: [5, 12, 20],
            14: [2, 15, 23],
            15: [11, 14, 16, 18],
            16: [15, 17, 19],
            17: [12, 16, 20],
            18: [10, 15, 19, 21],
            19: [16, 18, 22],
            20: [13, 17, 23],
            21: [9, 18, 22],
            22: [19, 21, 23],
            23: [14, 20, 22],
        }
