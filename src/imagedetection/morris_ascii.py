from __future__ import annotations
from typing import Dict, Optional, Tuple, List


NODE_POS: Dict[int, Tuple[int, int]] = {
    0: (0, 1),   1: (0, 13),  2: (0, 25),
    3: (2, 5),   4: (2, 13),  5: (2, 21),
    6: (4, 9),   7: (4, 13),  8: (4, 17),
    9: (6, 1),  10: (6, 5),  11: (6, 9),  12: (6, 17), 13: (6, 21), 14: (6, 25),
    15: (8, 9), 16: (8, 13), 17: (8, 17),
    18: (10, 5), 19: (10, 13), 20: (10, 21),
    21: (12, 1), 22: (12, 13), 23: (12, 25),
}

EDGES: List[Tuple[int, int]] = [
    
    (0, 1), (1, 2),
    (3, 4), (4, 5),
    (6, 7), (7, 8),
    (9, 10), (10, 11),
    (12, 13), (13, 14),
    (15, 16), (16, 17),
    (18, 19), (19, 20),
    (21, 22), (22, 23),

    (0, 9), (9, 21),
    (3, 10), (10, 18),
    (6, 11), (11, 15),
    (1, 4), (4, 7), (7, 16), (16, 19), (19, 22),
    (8, 12), (12, 17),
    (5, 13), (13, 20),
    (2, 14), (14, 23),
]


def render_morris_ascii(
    state: Optional[Dict[int, int]] = None,
    mode: str = "index",   # "index" oder "value"
) -> str:
    
    H, W = 13, 27
    canvas = [[" " for _ in range(W)] for _ in range(H)]


    for a, b in EDGES:
        ra, xa = NODE_POS[a]
        rb, xb = NODE_POS[b]

        if ra == rb:
            y = ra
            x1 = min(xa, xb) + 1
            x2 = max(xa, xb) - 2
            for x in range(x1, x2 + 1):
                canvas[y][x] = " "
        elif xa == xb:
            x = xa
            y1 = min(ra, rb) + 1
            y2 = max(ra, rb) - 1
            for y in range(y1, y2 + 1):
                canvas[y][x] = " "
        else:
            raise ValueError("Edge must be horizontal or vertical")


    for idx, (r, x_center) in NODE_POS.items():
        if mode == "index" or state is None:
            label = f"{idx:2d}"
        elif mode == "value":
            key = f"{idx:02d}" 
            v = state.get(idx, -1)
            label = f"{v:2d}"     # -1 / 0 / 1
        else:
            raise ValueError("mode must be 'index' or 'value'")

        c = x_center - 1
        canvas[r][c] = label[0]
        canvas[r][c + 1] = label[1]

    return "\n".join("".join(row).rstrip() for row in canvas)
