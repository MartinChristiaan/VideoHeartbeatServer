from server import create_server

import video_capture
import time
import cv2
import numpy as np

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from skinclassifier import SkinClassifier
from facetracker import FaceTracker
from rppgsensor import SimplePPGSensor,SimpleForeheadSensor,RegionSensor

from pulsedetector import PulseDetector
from framecapture import WebcamCapture
from enum import Enum

class VideoOutput(Enum):
     Source = 1
     PostFace = 2
     PostSkin = 3
class PulseDetectionMethod(Enum):
     Chrominance = 1
     PBV = 2

class Main:
    def __init__(self):
        self.frameCapture = WebcamCapture() #Stationary(1)
        self.SkinClassifier = SkinClassifier()
        self.faceTracker = FaceTracker()
        self.sensor = RegionSensor(self.frameCapture)
        
        self.pulseDetector = PulseDetector(self.frameCapture.fs)
        self.fps =  0
        self.tprev = 0
        self.display = VideoOutput.PostSkin
        self.useChrominance = PulseDetectionMethod.Chrominance

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
        
        self.pulseDetector.detect_pulse(fs,self.sensor.rppg)
        self.fps = 1/(time.time() - self.tprev)
        self.tprev = time.time()

        if self.display == VideoOutput.PostSkin:
           return skin
        elif self.display == VideoOutput.PostFace:
            return face
        else:
            return frame
        
main = Main()
#serialization.LoadFromJson(main.SkinClassifier)
video_capture.main = main

            #host="0.0.0.0"

if __name__ == '__main__':
    app = create_server([main,main.SkinClassifier,main.pulseDetector,main.faceTracker],lambda : video_capture.Camera())
    app.run(threaded = True)

