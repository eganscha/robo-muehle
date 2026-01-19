import cv2
import numpy as np

def _resize_to_height(img, h):
    if img is None:
        return None
    H, W = img.shape[:2]
    if H == h:
        return img
    scale = h / H
    return cv2.resize(img, (int(W * scale), h), interpolation=cv2.INTER_LINEAR)

def _hstack_safe(a, b):
    if a is None:
        return b
    if b is None:
        return a
    h = max(a.shape[0], b.shape[0])
    a2 = _resize_to_height(a, h)
    b2 = _resize_to_height(b, h)
    return np.hstack([a2, b2])