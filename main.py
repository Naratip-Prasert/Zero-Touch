import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

clicking = False
dwell_start = None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            x = int(handLms.landmark[8].x * screen_w)
            y = int(handLms.landmark[8].y * screen_h)

            pyautogui.moveTo(x, y, duration=0.05)

            thumb = handLms.landmark[4]
            index = handLms.landmark[8]

            dist = np.hypot(thumb.x - index.x, thumb.y - index.y)

            if dist < 0.03:
                if not clicking:
                    pyautogui.click()
                    clicking = True
            else:
                clicking = False

            center_x = int(index.x * w)
            center_y = int(index.y * h)

            if dwell_start is None:
                dwell_start = time.time()

            dwell_time = time.time() - dwell_start

            cv2.circle(img, (center_x, center_y), 20, (0, 255, 0), 2)
            cv2.putText(img, f"{round(dwell_time,1)}s",
                        (center_x-20, center_y-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

            if dwell_time > 1.5:
                pyautogui.click()
                dwell_start = None

    else:
        dwell_start = None

    cv2.imshow("Zero Touch Demo", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()