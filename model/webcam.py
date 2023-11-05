from typing import Any
import cv2 as cv
from PyQt5.QtCore import  QTimer

media_width, media_height = 500, 400


class Webcam():
    def __init__(self, app) -> None:
        self.app = app
        self.webcam = cv.VideoCapture(0)  # Use the default webcam (change the index if you have multiple webcams)
        self.webcam.set(cv.CAP_PROP_FRAME_WIDTH, media_width)
        self.webcam.set(cv.CAP_PROP_FRAME_HEIGHT, media_height)
    
    def start(self):
        self.app
        self.app.timer = QTimer(self)
        self.app.timer.timeout.connect(self.update_frame)
        self.app.timer.start(10)  # Adjust the time interval (ms) as needed
        self.app.start_webcam_button.setEnabled(False)
        self.app.stop_webcam_button.setEnabled(True)

    def stop(self):
        if self.app.timer:
            self.app.timer.stop()
        self.app.start_webcam_button.setEnabled(True)
        self.app.stop_webcam_button.setEnabled(False)
        self.app.webcam = None
        self.app.image_label.clear()

# def start_webcam(self):
#     self.initCamera()
#     self.timer = QTimer(self)
#     self.timer.timeout.connect(self.update_frame)
#     self.timer.start(10)  # Adjust the time interval (ms) as needed
#     self.start_webcam_button.setEnabled(False)
#     self.stop_webcam_button.setEnabled(True)

# def initCamera(self):
#     self.webcam = cv.VideoCapture(0)  # Use the default webcam (change the index if you have multiple webcams)
#     self.webcam.set(cv.CAP_PROP_FRAME_WIDTH, media_width)
#     self.webcam.set(cv.CAP_PROP_FRAME_HEIGHT, media_height)

# def stop_webcam(self):
#     if self.timer:
#         self.timer.stop()
#     self.start_webcam_button.setEnabled(True)
#     self.stop_webcam_button.setEnabled(False)
#     self.webcam = None
#     self.image_label.clear()