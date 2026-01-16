import numpy as np

def stone_centers(results0, conf_thres=0.25):

    if results0.boxes is None or len(results0.boxes) == 0:
        return []

    xywh = results0.boxes.xywh.detach().cpu().numpy() # in px
    conf = results0.boxes.conf.detach().cpu().numpy()
    cls  = results0.boxes.cls.detach().cpu().numpy().astype(int)

    out = []
    for (x, y, w, h), c, k in zip(xywh, conf, cls):
        if c < conf_thres:
            continue
        out.append((k, float(c), float(x), float(y)))
    return out
