# "# Zero-Touch"

This project is a computer vision system that allows users to control a computer using hand gestures via a webcam.

The system uses MediaPipe to detect hand landmarks and translate gestures into actions such as moving the cursor, clicking, scrolling, and other interactions.

## Features

- Move cursor using index finger  
- Pinch gesture for click  
- Dwell (hold) for double click  
- Swipe gesture for scrolling  
- Open palm to activate system  
- Fist gesture to deactivate system

## How It Works

The webcam captures hand movements, then MediaPipe processes the image to extract hand landmarks.  
These landmarks are used to detect gestures, which are mapped to mouse and keyboard actions in real time.

## Usage

### Install:
```bash
python main.py
python kiosk_app.py
```

### Run
```bash
pip install mediapipe==0.10.11
pip install opencv-python pyautogui numpy
```

### Camera Setup

You can use either a built-in webcam or a phone/iPad as an external webcam.

For phone/iPad camera, this project is tested with **Iriun Webcam**.

Steps:
1. Install **Iriun Webcam** on your phone/iPad.
2. Install **Iriun Webcam client** on your computer.
3. Connect the phone/iPad to the computer using USB.
4. Open Iriun Webcam on both devices.
5. Run the project.

### Notes

If the phone camera is not detected, change the camera index in `config.py`:

```python
CAMERA_PC = 0
CAMERA_PHONE = 1
```

Try changing `CAMERA_PHONE` to `2` or `3` if needed.