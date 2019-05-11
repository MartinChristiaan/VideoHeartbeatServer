from server import create_server
from UIInstructions import *
import video_capture
import time
import cv2
import numpy as np
import serialization
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from skinclassifier import SkinClassifier
from facetracker import FaceTracker
from rppgsensor import SimplePPGSensor
from signalprocessor import extract_pulse_chrominance,extract_pulse_PBV
from evaluator import Evaluator
from framecapture import WebcamCapture,Stationary,MixedMotion

class Main:
    def __init__(self):
        self.frameCapture = WebcamCapture() #Stationary(1)
        self.SkinClassifier = SkinClassifier()
        self.faceTracker = FaceTracker()
        self.sensor = SimplePPGSensor(self.frameCapture)
        
        self.evaluator = Evaluator(self.frameCapture.fs)
        self.fps =  0
        self.tprev = 0
        self.display = "Source"
        self.detectionMethod = 0

    def resetMeasurement(self):
        print("Reseting measurements")
        self.faceTracker.resetTracker()
        self.sensor.reset(self.frameCapture)
        self.frameCapture.timestamps = []

    def main(self):
        frame = self.frameCapture.get_frame()
        
        fs = self.frameCapture.fs
        face = []
        face = self.faceTracker.crop_to_face(frame)

        skin,pixels = self.SkinClassifier.apply_skin_classifier(face)
        self.sensor.sense_ppg(skin,pixels)
        
        if self.detectionMethod == 0:
            normalized_amplitude = extract_pulse_chrominance(self.frameCapture.fs,self.sensor.rppg)
        else:
            normalized_amplitude = extract_pulse_PBV(self.frameCapture.fs,self.sensor.rppg)
                
        self.evaluator.evaluate(fs,normalized_amplitude)
        self.fps = 1/(time.time() - self.tprev)
        self.tprev = time.time()

        if self.display == 2:
           return skin
        elif self.display == 1:
            return face
        else:
            return frame
        
main = Main()
#serialization.LoadFromJson(main.SkinClassifier)
video_capture.main = main

            #host="0.0.0.0"

if __name__ == '__main__':
    app = create_server([main,main.SkinClassifier,main.evaluator],lambda : video_capture.Camera())
    app.run(threaded = True)

