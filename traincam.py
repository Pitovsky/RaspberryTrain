import sys
import threading
import time
from random import random

import numpy as np
import cv2
import keras
from keras.models import load_model
from keras.layers import Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.preprocessing import image

import tensorflow as tf

video_stream_path = 0 # 'videos/test4.mp4' #'http://192.168.0.190:8080/stream/video.mjpeg'

class TrainCam:
    
    def __init__(self):
        self.danger = False
        self.prev_danger = False
        self.running = True
        self.cap = cv2.VideoCapture(video_stream_path)
        self.graph = tf.get_default_graph() 
        self.model = self.load_model()
        self.job = threading.Thread(target=self.cam_check)
    
    def load_model(self):
        #model = keras.applications.resnet50.ResNet50(weights=None)
        #model.layers.pop()
        #last = model.layers[-1].output
        #x = Dense(3, activation="softmax")(last) # 3 classes
        #finetuned_model = Model(model.input, x)
        #finetuned_model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
        #finetuned_model.load_weights('classification.h5')
        #return finetuned_model
        return load_model('classification_79.h5') # works only for keras>=2.3.x
    
    def cam_check(self):
        while self.running:
            ret, frame = self.cap.read()
            #cv2.imshow('frame', frame)
            #k = cv2.waitKey(5) & 0xff
            cur_danger = self.make_danger_prediction(frame)
            print(frame.shape, cur_danger)
            if cur_danger == self.prev_danger:
                self.danger = cur_danger
            self.prev_danger = cur_danger
    
    def make_danger_prediction(self, frame):
        x = image.img_to_array(frame[16:240,48:272])
        x = np.expand_dims(x, axis=0)
        with self.graph.as_default():
            preds = self.model.predict(x)
        return np.argmax(preds) != 0 # 0 is 'clear' class

    
    def start(self):
        self.job.start()
    
    def is_dangerous(self):
        return self.danger
    
    def stop(self):
        self.running = False
        self.job.join()
        self.cap.release()
