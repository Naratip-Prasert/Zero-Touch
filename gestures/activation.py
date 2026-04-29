def is_finger_extended(lm, tip_id, pip_id):
    return lm[tip_id].y < lm[pip_id].y


def is_open_palm(handLms):
    lm = handLms.landmark

    fingers = [
        is_finger_extended(lm, 8, 6),    # index
        is_finger_extended(lm, 12, 10),  # middle
        is_finger_extended(lm, 16, 14),  # ring
        is_finger_extended(lm, 20, 18),  # pinky
    ]

    return sum(fingers) >= 4