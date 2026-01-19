import numpy as np
from PIL import Image, ImageDraw, ImageOps

MUEHLE_INDEX_MAP = np.array(
    [
        [1, 0, 0, 2, 0, 0, 3],
        [0, 4, 0, 5, 0, 6, 0],
        [0, 0, 7, 8, 9, 0, 0],
        [10, 11, 12, 0, 13, 14, 15],
        [0, 0, 16, 17, 18, 0, 0],
        [0, 19, 0, 20, 0, 21, 0],
        [22, 0, 0, 23, 0, 0, 24],
    ],
    dtype=np.int8,
)


def create_stone(
    size: int,
    color: tuple[int, int, int],
    outline: bool = True,
    outline_color: tuple[int, int, int, int] = (0, 0, 0, 200),
    outline_width: int = 2,
) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = outline_width // 2
    bbox = (
        pad,
        pad,
        size - pad - 1,
        size - pad - 1,
    )

    draw.ellipse(
        bbox,
        fill=(*color, 255),
        outline=outline_color if outline else None,
        width=outline_width if outline else 0,
    )

    return img


def state24_to_points(state: np.ndarray) -> np.ndarray:
    assert state.shape == (24,)
    assert state.dtype == np.int8

    points = np.zeros((7, 7), dtype=np.int8)

    for idx in range(24):
        pos = idx + 1
        value = state[idx]
        if value == 0:
            continue

        y, x = np.argwhere(MUEHLE_INDEX_MAP == pos)[0]
        points[y, x] = value

    return points


def calc_coords_muhle(i: int, j: int):
    BOARD_SIZE = 1024
    GRID_SIZE = 6
    MARGIN = 110
    PIECE_SIZE = 96

    step = (BOARD_SIZE - 2 * MARGIN) // GRID_SIZE

    x = MARGIN + j * step
    y = MARGIN + i * step

    return (
        x,
        y,
        PIECE_SIZE,
        PIECE_SIZE,
        "center",
        "center",
    )


def load_board():
    board = Image.open("board.jpg").convert("RGBA")

    w, h = board.size
    hw, hh = w // 2, h // 2

    tl = board.crop((0, 0, hw, hh))

    tr = ImageOps.mirror(tl)
    bl = ImageOps.flip(tl)
    br = ImageOps.flip(tr)

    clean = Image.new("RGBA", (w, h))

    clean.paste(tl, (0, 0))
    clean.paste(tr, (hw, 0))
    clean.paste(bl, (0, hh))
    clean.paste(br, (hw, hh))

    return clean


board = load_board()


STONE_SIZE = 96

white_stone = create_stone(
    size=STONE_SIZE,
    color=(235, 235, 235),
)

black_stone = create_stone(
    size=STONE_SIZE,
    color=(40, 40, 40),
)

pieces = [white_stone, black_stone]
