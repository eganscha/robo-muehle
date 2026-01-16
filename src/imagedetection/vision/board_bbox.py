import numpy as np


def best_board_box(results0) -> tuple[int, int, int, int] | None:
    if results0.boxes is None or len(results0.boxes) == 0:
        return None

    boxes = results0.boxes
    conf = boxes.conf.detach().cpu().numpy()
    xyxy = boxes.xyxy.detach().cpu().numpy()

    i = int(np.argmax(conf))
    x1, y1, x2, y2 = xyxy[i]
    return int(x1), int(y1), int(x2), int(y2)


def corners_from_bbox(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]