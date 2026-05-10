import time
from collections import deque
from config import SWIPE_THRESHOLD, SWIPE_COOLDOWN

y_history = deque(maxlen=5)

swipe_ready = True


def detect_swipe(current_y, last_swipe_time):

    global swipe_ready

    now = time.time()

    y_history.append(current_y)

    if len(y_history) < 5:
        return None, last_swipe_time

    delta_y = y_history[-1] - y_history[0]

    # ===== reset zone =====
    if abs(delta_y) < 15:
        swipe_ready = True
        return None, last_swipe_time

    # ยังไม่พร้อม swipe ใหม่
    if not swipe_ready:
        return None, last_swipe_time

    # cooldown
    if now - last_swipe_time < SWIPE_COOLDOWN:
        return None, last_swipe_time

    # ===== swipe =====
    if delta_y > SWIPE_THRESHOLD:
        swipe_ready = False
        y_history.clear()
        return "up", now

    elif delta_y < -SWIPE_THRESHOLD:
        swipe_ready = False
        y_history.clear()
        return "down", now

    return None, last_swipe_time