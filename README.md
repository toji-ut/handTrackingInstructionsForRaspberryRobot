# Hand Gesture Recognition and GPIO Control

This project enables hand gesture recognition using MediaPipe and OpenCV on a Mac to control GPIO pins on a Raspberry Pi over a local network.

## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- MediaPipe (`pip install mediapipe`)
- RPi.GPIO (for Raspberry Pi, `pip install RPi.GPIO`)

## Usage
- Run main.py on your computer with a webcam.
- Run robot.py on the Raspberry PI
## Perform gestures:
- Thumb to index finger: 'f' (forward).
- Thumb to middle finger: 'b' (backward).
- Thumb to ring finger: 's' (stop).
- Thumb to pinky finger: 'e' (exit).
## Detected gestures send commands to connected Raspberry Pi.
Receives commands ('f', 'b', 's', 'e') from the computer to control GPIO pins.
