import time
from config import SWIPE_THRESHOLD, SWIPE_COOLDOWN

def detect_swipe(delta_y, last_swipe_time):
    now = time.time()

    if now - last_swipe_time < SWIPE_COOLDOWN:
        return None, last_swipe_time

    if delta_y > SWIPE_THRESHOLD:
        return "down", now

    elif delta_y < -SWIPE_THRESHOLD:
        return "up", now

    return None, last_swipe_time