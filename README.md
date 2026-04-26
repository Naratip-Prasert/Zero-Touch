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

Install:
- pip install mediapipe==0.10.11
- pip install opencv-python pyautogui numpy
---
RUN: 
- python main.py
- python kiosk_app.py
---
