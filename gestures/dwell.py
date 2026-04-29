import time
from config import DWELL_MOVEMENT_THRESHOLD

def update_dwell(dwell_start, movement, is_swiping):
    if is_swiping:
        return None, 0

    if movement < DWELL_MOVEMENT_THRESHOLD:
        if dwell_start is None:
            dwell_start = time.time()
    else:
        dwell_start = None

    if dwell_start is not None:
        dwell_time = time.time() - dwell_start
    else:
        dwell_time = 0

    return dwell_start, dwell_time