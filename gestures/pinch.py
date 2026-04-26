import numpy as np

pinch_frames = 0

def distance(a, b):
    return np.hypot(a.x - b.x, a.y - b.y)

def is_pinch(handLms):
    global pinch_frames

    lm = handLms.landmark

    thumb_tip = lm[4]
    index_tip = lm[8]
    wrist = lm[0]
    middle_base = lm[9]

    hand_size = distance(wrist, middle_base)
    pinch_dist = distance(thumb_tip, index_tip)

    threshold = hand_size * 0.14

    if pinch_dist < threshold:
        pinch_frames += 1
    else:
        pinch_frames = 0

    return pinch_frames >= 2