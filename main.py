import cv2
import pyautogui
import time

from tracking.hand_tracker import detect_hand, draw_hand
from gestures.pinch import is_pinch
from gestures.swipe import detect_swipe
from controller.actions import move_cursor, click, swipe_action
from config import FIST_HOLD_TIME
from gestures.activation import is_open_palm
from gestures.deactivation import is_fist

def init_camera(source):
    if isinstance(source, int):
        cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(source)

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 15)

    return cap
screen_w, screen_h = pyautogui.size()

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

CAMERA_PHONE = "http://10.201.217.42:4747/video"
CAMERA_PC = 0

current_source = CAMERA_PC
cap = init_camera(current_source)

def switch_camera():
    global cap, current_source

    cap.release()

    if current_source == CAMERA_PHONE:
        current_source = CAMERA_PC
    else:
        current_source = CAMERA_PHONE

    cap = init_camera(current_source)

    print(f"Switched to: {current_source}")

screen_w, screen_h = pyautogui.size()

pinch_lock_x, pinch_lock_y = None, None
clicking = False

# เริ่มต้น/ปิดระบบมือ
system_active = False
activation_start = None
last_hand_seen = time.time()
fist_start = None

prev_x, prev_y = 0, 0
swipe_cooldown = 0
smooth_screen_x, smooth_screen_y = 0, 0

while True:
    for _ in range(3):
        cap.grab()

    ret, frame = cap.read()

    if not ret:
        print("No frame")
        continue

    frame = cv2.resize(frame, (640, 480))


    img = cv2.flip(frame, 1)
    img = cv2.convertScaleAbs(img, alpha=1.2, beta=20)
    h, w, _ = img.shape

    result = detect_hand(img)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            draw_hand(img, handLms)

            thumb = handLms.landmark[4]
            index = handLms.landmark[8]
            
            # ===== Deactivation Logic =====
            last_hand_seen = time.time()

            if system_active:
                if is_fist(handLms) and not is_pinch(handLms):
                    if fist_start is None:
                        fist_start = time.time()

                    fist_time = time.time() - fist_start

                    cv2.putText(
                        img,
                        f"Hold fist to deactivate: {round(fist_time,1)}s",
                        (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )

                    if fist_time > FIST_HOLD_TIME:
                        system_active = False
                        fist_start = None
                        dwell_start = None
                        activation_start = None
                        clicking = False

                        cv2.putText(
                            img,
                            "System Deactivated",
                            (30, 130),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2
                        )

                        continue

                else:
                    fist_start = None
            
            # ===== Activation Logic =====
            active_gesture = is_open_palm(handLms)

            if not system_active:
                if active_gesture:
                    if activation_start is None:
                        activation_start = time.time()

                    activation_time = time.time() - activation_start

                    cv2.putText(
                        img,
                        f"Hold to activate: {round(activation_time,1)}s",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        2
                    )

                    if activation_time > 3:
                        system_active = True
                        activation_start = None

                else:
                    activation_start = None

                continue

            raw_x = int(index.x * screen_w)
            raw_y = int(index.y * screen_h)

            # วัดความเร็วการเคลื่อนที่
            speed = abs(raw_x - smooth_screen_x) + abs(raw_y - smooth_screen_y)

            # ปรับ smoothing ตาม speed
            if speed > 50:
                alpha = 0.5   # เร็ว
            elif speed > 20:
                alpha = 0.35  # กลาง
            else:
                alpha = 0.2   # นิ่ง

            smooth_screen_x = int(alpha * raw_x + (1 - alpha) * smooth_screen_x)
            smooth_screen_y = int(alpha * raw_y + (1 - alpha) * smooth_screen_y)

            # ===== Cursor Move =====
            if not is_pinch(handLms):
                move_cursor(smooth_screen_x, smooth_screen_y)

            center_x = int(index.x * w)
            center_y = int(index.y * h)

            # ===== Pinch Click =====
            if is_pinch(handLms):
                if not clicking:
                    pinch_lock_x = smooth_screen_x
                    pinch_lock_y = smooth_screen_y

                    move_cursor(pinch_lock_x, pinch_lock_y)
                    click()

                    clicking = True
            else:
                clicking = False
                pinch_lock_x, pinch_lock_y = None, None

            # ===== Swipe =====
            delta_y = center_y - prev_y
            direction, swipe_cooldown = detect_swipe(delta_y, swipe_cooldown)

            is_swiping = direction is not None

            if direction:
                swipe_action(direction)

            prev_x, prev_y = center_x, center_y

            # ===== UI =====
            cv2.circle(img, (center_x, center_y), 20, (0, 255, 0), 2)
            cv2.putText(
                img,
                "Cursor",
                (center_x - 40, center_y - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    else:
        if time.time() - last_hand_seen > 3.0:
            system_active = False
            dwell_start = None
            clicking = False
            fist_start = None
            activation_start = None

            cv2.putText(
                img,
                "No hand detected - system off",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

    preview = cv2.resize(img, (480, 360))
    cv2.imshow("Camera Preview", preview)
    cv2.moveWindow("Camera Preview", 20, 20)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break
    elif key == ord('c'):  # กด C เพื่อสลับกล้อง
        switch_camera()

cap.release()
cv2.destroyAllWindows()