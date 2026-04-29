import cv2
import platform
from config import FRAME_HEIGHT, FRAME_WIDTH

def init_camera(source):
    if isinstance(source, int):
        if platform.system() == "Windows":
            cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(source)
    else:
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"❌ Cannot open camera: {source}")
        return cap

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 15)

    return cap


def switch_camera(cap, current_source, cam_pc, cam_phone):
    old_source = current_source
    new_source = cam_phone if current_source == cam_pc else cam_pc

    cap.release()
    new_cap = init_camera(new_source)

    if not new_cap.isOpened():
        print("❌ camera failed → revert")
        return init_camera(old_source), old_source

    print(f"Switched to: {new_source}")
    return new_cap, new_source