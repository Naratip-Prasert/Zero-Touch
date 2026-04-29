from config import CAMERA_MIN_X, CAMERA_MAX_X, CAMERA_MIN_Y, CAMERA_MAX_Y

def map_to_screen(index, screen_w, screen_h):
    mapped_x = (index.x - CAMERA_MIN_X) / (CAMERA_MAX_X - CAMERA_MIN_X)
    mapped_y = (index.y - CAMERA_MIN_Y) / (CAMERA_MAX_Y - CAMERA_MIN_Y)

    mapped_x = max(0, min(1, mapped_x))
    mapped_y = max(0, min(1, mapped_y))

    raw_x = int(mapped_x * screen_w)
    raw_y = int(mapped_y * screen_h)

    return raw_x, raw_y