import cv2

_CAP = None

def get_camera(index: int = 0):
    global _CAP
    if _CAP is None:
        _CAP = cv2.VideoCapture(index)
        if not _CAP.isOpened():
            raise RuntimeError(f"Could not open camera {index}")
    return _CAP

def get_frame_bgr():
    cap = get_camera()
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Could not read camera frame")
    return frame

def close_camera():
    global _CAP
    if _CAP is not None:
        _CAP.release()
        _CAP = None