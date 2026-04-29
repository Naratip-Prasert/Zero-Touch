import numpy as np


def distance(a, b):
    return np.hypot(a.x - b.x, a.y - b.y)


def make_point(x, y):
    class Point:
        pass

    point = Point()
    point.x = x
    point.y = y
    return point


def is_fist(handLms):
    lm = handLms.landmark
    wrist = lm[0]

    palm_center = make_point(
        (lm[0].x + lm[5].x + lm[9].x + lm[13].x + lm[17].x) / 5,
        (lm[0].y + lm[5].y + lm[9].y + lm[13].y + lm[17].y) / 5
    )

    palm_size = distance(wrist, lm[9])

    index_extended = distance(lm[8], wrist) > distance(lm[6], wrist) * 1.15
    if index_extended:
        return False

    folded_count = 0
    for tip_id in [8, 12, 16, 20]:
        if distance(lm[tip_id], palm_center) < palm_size * 0.65:
            folded_count += 1

    return folded_count >= 3