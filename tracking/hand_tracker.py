import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.7
)

def detect_hand(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb.flags.writeable = False
    result = hands.process(rgb)
    return result

def draw_hand(img, hand_landmarks):
    mp_draw.draw_landmarks(
        img,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS
    )