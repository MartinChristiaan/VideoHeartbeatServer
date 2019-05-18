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
from framecapture import WebcamCapture,Recorded
from enum import Enum

class VideoOutput(Enum):
     Source = 1
     PostFace = 2
     PostSkin = 3
class PulseDetectionMethod(Enum):
     Chrominance = 1
     PBV = 2

class Recorder():
    def __init__(self,framecapture):
        self.enabled = False
        self.previousFrames = []
        self.framecap = framecapture
    def record(self,frame):
        if self.enabled:
            self.previousFrames += [frame]
            no_fr = len(self.previousFrames)
            if no_fr%10 == 0:
                print("{0} frames recorded".format(no_fr))
            
    def save_recording(self):
        timestamps = self.framecap.timestamps
        f = open('recording/timestamps.txt','w')
        f.write(",".join([str(x) for x in timestamps]))
        for i,fr in enumerate(self.previousFrames):
            cv2.imwrite("recording/{0}.jpg".format(i),fr)
        self.previousFrames = []
            
        

class Main:
    def __init__(self):
        self.frameCapture = WebcamCapture() #Recorded(0) #Stationary(1)
        self.SkinClassifier = SkinClassifier()
        self.faceTracker = FaceTracker()
        self.sensor = SimplePPGSensor(self.frameCapture)
        
        self.pulseDetector = PulseDetector(self.frameCapture.fs)
        self.fps =  0
        self.tprev = 0
        self.display = VideoOutput.PostSkin
        self.useChrominance = PulseDetectionMethod.Chrominance
        self.recorder = Recorder(self.frameCapture)

    def resetMeasurement(self):
        print("Reseting measurements")
        self.faceTracker.resetTracker()
        self.sensor.reset(self.frameCapture)
        self.frameCapture.timestamps = []

    def main(self):
        frame = self.frameCapture.get_frame()
        
        fs = self.frameCapture.fs
        #face = frame
        face = self.faceTracker.crop_to_face(frame)
        #skin = face
        
        skin,pixels = self.SkinClassifier.apply_skin_classifier(face)
        self.sensor.sense_ppg(skin,pixels)
        


                
        self.pulseDetector.detect_pulse(fs,self.sensor.rppg)
        self.fps = 1/(time.time() - self.tprev)
        self.tprev = time.time()
        
   

            #cv2.imwrite("Test.jpg",frame)
            
        displayframe = []
        if self.display == VideoOutput.PostSkin:
           displayframe = skin
        elif self.display == VideoOutput.PostFace:
            displayframe = face
        else:
            displayframe = frame
        
        self.recorder.record(displayframe)
        return displayframe
        
main = Main()
#serialization.LoadFromJson(main.SkinClassifier)
video_capture.main = main

            #host="0.0.0.0"

if __name__ == '__main__':
    app = create_server([main,main.SkinClassifier,main.pulseDetector,main.faceTracker,main.recorder],lambda : video_capture.Camera())
    app.run(threaded = True)

