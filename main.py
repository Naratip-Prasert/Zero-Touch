import cv2
import pyautogui
import time

from tracking.hand_tracker import detect_hand, draw_hand
from tracking.camera import init_camera, switch_camera
from gestures.pinch import is_pinch
from gestures.swipe import detect_swipe
from controller.actions import move_cursor, click, swipe_action
from controller.mapping import map_to_screen
from controller.smoothing import smooth_move
from config import FIST_HOLD_TIME,FRAME_HEIGHT, FRAME_WIDTH
from gestures.activation import is_open_palm
from gestures.deactivation import is_fist

screen_w, screen_h = pyautogui.size()

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

CAMERA_PHONE = 1
CAMERA_PC = 0

current_source = CAMERA_PC
cap = init_camera(current_source)

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

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))


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

            raw_x, raw_y = map_to_screen(index, screen_w, screen_h)
            smooth_screen_x, smooth_screen_y = smooth_move(
                raw_x,
                raw_y,
                smooth_screen_x,
                smooth_screen_y
            )

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
    elif key == ord('c'):
        cap, current_source = switch_camera(
            cap,
            current_source,
            CAMERA_PC,
            CAMERA_PHONE
        )

cap.release()
cv2.destroyAllWindows()