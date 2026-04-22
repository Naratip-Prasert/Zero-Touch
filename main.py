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
last_click_time = 0
cooldown = 1.0  # วินาที
prev_x, prev_y = 0, 0
swipe_cooldown = 0

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

            pyautogui.moveTo(x, y)

            thumb = handLms.landmark[4]
            index = handLms.landmark[8]

            dist = np.hypot(thumb.x - index.x, thumb.y - index.y)

            if dist < 0.05:
                if not clicking:
                    pyautogui.click()
                    clicking = True
            else:
                clicking = False

            # ===== Dwell Logic =====
            center_x = int(index.x * w)
            center_y = int(index.y * h)

            # ===== Swipe Logic =====
            current_y = center_y
            delta_y = current_y - prev_y
            now = time.time()

            is_swiping = False

            # ต้องเร็วจริง ถึงจะ swipe
            if abs(delta_y) > 60 and now - swipe_cooldown > 0.5:
                is_swiping = True
                
                if delta_y > 0:
                    pyautogui.scroll(-500)
                else:
                    pyautogui.scroll(500)

                swipe_cooldown = now

            movement = abs(center_x - prev_x) + abs(center_y - prev_y)
            
            #ถ้ากำลัง swipe ไม่ต้องนับ dwell
            if is_swiping:
                dwell_start = None

            else:
                # ถ้านิ่งจริงถึงนับ
                if movement < 20:
                    if dwell_start is None:
                        dwell_start = time.time()
                else:
                    dwell_start = None

            dwell_time = time.time() - dwell_start if dwell_start else 0

            prev_x, prev_y = center_x, center_y
            print("dwell:", dwell_time)

            # วาด UI
            cv2.circle(img, (center_x, center_y), 20, (0, 255, 0), 2)
            cv2.putText(img, f"{round(dwell_time,1)}s",
                        (center_x-20, center_y-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

            # ===== Double Click =====
            now = time.time()
            
            if dwell_time > 3.0 and now - last_click_time > cooldown:
                pyautogui.doubleClick()
                last_click_time = now
                dwell_start = None

    else:
        if dwell_start is not None:
            dwell_time = time.time() - dwell_start

        dwell_start = None

    cv2.imshow("Zero Touch Demo", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()