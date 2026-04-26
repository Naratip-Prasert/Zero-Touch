import cv2
import pyautogui
import time

from tracking.hand_tracker import detect_hand, draw_hand
from gestures.pinch import is_pinch
from gestures.dwell import update_dwell
from gestures.swipe import detect_swipe
from controller.actions import move_cursor, click, double_click, swipe_action
from config import DWELL_TIME, ACTION_COOLDOWN

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

clicking = False
dwell_start = None
last_action_time = 0

prev_x, prev_y = 0, 0
swipe_cooldown = 0

while True:
    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    result = detect_hand(img)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            draw_hand(img, handLms)

            thumb = handLms.landmark[4]
            index = handLms.landmark[8]

            screen_x = int(index.x * screen_w)
            screen_y = int(index.y * screen_h)

            move_cursor(screen_x, screen_y)

            center_x = int(index.x * w)
            center_y = int(index.y * h)

            # ===== Pinch Click =====
            if is_pinch(thumb, index):
                if not clicking:
                    click()
                    clicking = True
            else:
                clicking = False

            # ===== Swipe =====
            delta_y = center_y - prev_y
            direction, swipe_cooldown = detect_swipe(delta_y, swipe_cooldown)

            is_swiping = direction is not None

            if direction:
                swipe_action(direction)

            # ===== Dwell =====
            movement = abs(center_x - prev_x) + abs(center_y - prev_y)

            dwell_start, dwell_time = update_dwell(
                dwell_start,
                movement,
                is_swiping
            )

            now = time.time()

            if dwell_time > DWELL_TIME and now - last_action_time > ACTION_COOLDOWN:
                double_click()
                last_action_time = now
                dwell_start = None

            prev_x, prev_y = center_x, center_y

            # ===== UI =====
            cv2.circle(img, (center_x, center_y), 20, (0, 255, 0), 2)
            cv2.putText(
                img,
                f"Dwell: {round(dwell_time, 1)}s",
                (center_x - 40, center_y - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    else:
        dwell_start = None
        clicking = False

    cv2.imshow("Zero Touch Demo", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()