import cv2
import signal
import sys
import threading
import time
from random import random

video_stream_path = 0 #'http://192.168.0.190:8080/stream/video.mjpeg'

def is_frame_dangerous(frame):
    return random() > 0.97 # TODO

class TrainCam:
    
    def __init__(self):
        self.cap = cv2.VideoCapture(video_stream_path)
        self.danger = False
        self.running = True
        self.job = threading.Thread(target=self.cam_check)
    
    def cam_check(self):
        while self.running:
            ret, frame = self.cap.read()
            self.danger = is_frame_dangerous(frame)
    
    def start(self):
        self.job.start()
    
    def is_dangerous(self):
        return self.danger
    
    def stop(self):
        self.running = False
        self.job.join()
        self.cap.release()
