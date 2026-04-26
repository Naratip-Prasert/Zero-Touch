def is_fist(handLms):
    fingers_folded = []

    fingers_folded.append(handLms.landmark[8].y > handLms.landmark[6].y)
    fingers_folded.append(handLms.landmark[12].y > handLms.landmark[10].y)
    fingers_folded.append(handLms.landmark[16].y > handLms.landmark[14].y)
    fingers_folded.append(handLms.landmark[20].y > handLms.landmark[18].y)

    return sum(fingers_folded) >= 4