def is_open_palm(handLms):
    fingers = []

    # index finger
    fingers.append(handLms.landmark[8].y < handLms.landmark[6].y)

    # middle finger
    fingers.append(handLms.landmark[12].y < handLms.landmark[10].y)

    # ring finger
    fingers.append(handLms.landmark[16].y < handLms.landmark[14].y)

    # pinky
    fingers.append(handLms.landmark[20].y < handLms.landmark[18].y)

    return sum(fingers) >= 4