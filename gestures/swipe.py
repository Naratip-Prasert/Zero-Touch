import time
from config import SWIPE_THRESHOLD, SWIPE_COOLDOWN

def detect_swipe(delta_y, swipe_cooldown):
    now = time.time()

    if now - swipe_cooldown < SWIPE_COOLDOWN:
        return None, swipe_cooldown

    if delta_y > SWIPE_THRESHOLD:
        return "down", now

    if delta_y < -SWIPE_THRESHOLD:
        return "up", now

    return None, swipe_cooldown