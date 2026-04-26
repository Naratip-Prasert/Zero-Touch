import numpy as np
from config import PINCH_THRESHOLD

def is_pinch(thumb, index):
    dist = np.hypot(thumb.x - index.x, thumb.y - index.y)
    return dist < PINCH_THRESHOLD