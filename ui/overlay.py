import cv2


def draw_status(img, system_active, gesture=None, fps=None):
    h, w, _ = img.shape

    # กล่อง overlay มุมขวาบน
    x1, y1 = w - 230, 20
    x2, y2 = w - 20, 125

    cv2.rectangle(img, (x1, y1), (x2, y2), (20, 20, 20), -1)
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)

    status = "ACTIVE" if system_active else "INACTIVE"
    status_color = (0, 255, 0) if system_active else (0, 0, 255)

    cv2.putText(
        img,
        f"System: {status}",
        (x1 + 15, y1 + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        status_color,
        2
    )

    if gesture is not None:
        cv2.putText(
            img,
            f"Gesture: {gesture}",
            (x1 + 15, y1 + 62),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

    if fps is not None:
        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (x1 + 15, y1 + 94),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


def draw_cursor(img, x, y):
    cv2.circle(img, (x, y), 14, (0, 255, 0), 2)
    cv2.circle(img, (x, y), 4, (0, 255, 0), -1)