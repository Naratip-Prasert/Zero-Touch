from config import SMOOTHING_SLOW, SMOOTHING_MEDIUM, SMOOTHING_FAST

def smooth_move(raw_x, raw_y, prev_x, prev_y):
    speed = abs(raw_x - prev_x) + abs(raw_y - prev_y)

    if speed > 50:
        alpha = SMOOTHING_FAST
    elif speed > 20:
        alpha = SMOOTHING_MEDIUM
    else:
        alpha = SMOOTHING_SLOW

    smooth_x = int(alpha * raw_x + (1 - alpha) * prev_x)
    smooth_y = int(alpha * raw_y + (1 - alpha) * prev_y)

    return smooth_x, smooth_y