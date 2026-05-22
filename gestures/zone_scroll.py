import time

hold_start = None
active_zone = None
last_scroll_time = 0


def detect_zone_scroll(y, frame_h):
    global hold_start, active_zone, last_scroll_time

    now = time.time()

    top_zone = frame_h * 0.28
    bottom_zone = frame_h * 0.72

    # อยู่โซนบน
    if y < top_zone:
        zone = "top"

    # อยู่โซนล่าง
    elif y > bottom_zone:
        zone = "bottom"

    # อยู่กลาง = reset
    else:
        hold_start = None
        active_zone = None
        return None

    # ถ้าเปลี่ยนโซน ให้เริ่มจับเวลาใหม่
    if active_zone != zone:
        active_zone = zone
        hold_start = now
        return None

    # ต้องค้าง 2 วิ ก่อนเริ่มเลื่อน
    if now - hold_start < 2.0:
        return None

    # เลื่อนทุก 0.15 วิ
    if now - last_scroll_time < 0.3:
        return None

    last_scroll_time = now

    if zone == "top":
        return "up"

    if zone == "bottom":
        return "down"

    return None