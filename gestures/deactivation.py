import numpy as np

def distance(a, b):
    return np.hypot(a.x - b.x, a.y - b.y)

def is_fist(handLms):
    lm = handLms.landmark

    wrist = lm[0]

    # จุดกลางฝ่ามือ
    palm_center_x = (lm[0].x + lm[5].x + lm[9].x + lm[13].x + lm[17].x) / 5
    palm_center_y = (lm[0].y + lm[5].y + lm[9].y + lm[13].y + lm[17].y) / 5

    class Point:
        pass

    palm_center = Point()
    palm_center.x = palm_center_x
    palm_center.y = palm_center_y

    palm_size = distance(wrist, lm[9])

    # ถ้ามือนิ้วชี้ยังยื่นออกมา ไม่ใช่กำมือ
    index_extended = distance(lm[8], wrist) > distance(lm[6], wrist) * 1.15
    if index_extended:
        return False

    folded_count = 0

    finger_tips = [8, 12, 16, 20]

    for tip_id in finger_tips:
        tip = lm[tip_id]

        # กำมือจริง = ปลายนิ้วต้องเข้ามาใกล้กลางฝ่ามือ
        if distance(tip, palm_center) < palm_size * 0.65:
            folded_count += 1

    return folded_count >= 3