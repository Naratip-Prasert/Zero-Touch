import numpy as np
from config import PINCH_THRESHOLD

pinch_frames = 0

def is_pinch(thumb, index):
    global pinch_frames

    dist = np.hypot(thumb.x - index.x, thumb.y - index.y)

    if dist < PINCH_THRESHOLD:
        pinch_frames += 1
    else:
        pinch_frames = 0

    return pinch_frames >= 4