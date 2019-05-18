import cv2
import numpy as np
import torch
from enum import Enum
class ClassifierType(Enum):
     Manual = 1
     NeuralNet = 2
     
model=torch.load('modelfile.txt')
device = torch.device("cuda:0")

class SkinClassifier:
    def __init__(self):
        self.minh = 0
        self.mins = 40
        self.minv = 80
        self.maxh = 20
        self.maxs = 255
        self.maxv = 255
        self.elipse_size = 12
        self.blursize = 5
        self.erosions = 2
        self.dilations = 2

        self.num_skin_pixels = 0
        self.myy = 100
        self.enabled = False
        self.classifierType = ClassifierType.Manual
  

    def apply_skin_classifier(self,frame):
        if self.enabled:
            try:
                if self.classifierType == ClassifierType.Manual:
                    lower = np.array([self.minh, self.mins, self.minv], dtype = "uint8")
                    upper = np.array([self.maxh, self.maxs, self.maxv], dtype = "uint8")
                    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    skinMask = cv2.inRange(converted, lower, upper)
                else:
                    imre = frame.reshape(frame.shape[0] * frame.shape[1],3) 
                    imre = torch.tensor(imre, device=device,dtype = torch.float)    
                    skinMask = (model(imre)*255).detach().cpu().numpy().reshape(frame.shape[0],frame.shape[1]).astype("uint8")
    
                elipse_size = int(self.elipse_size)
                blursize = int(self.blursize)
                erotions = int(self.erosions)
                dilations = int(self.dilations)
                
                if elipse_size > 0:
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (elipse_size, elipse_size))
                    if erotions>0:
                        skinMask = cv2.erode(skinMask, kernel, iterations = erotions)
                    if dilations>0:
                        skinMask = cv2.dilate(skinMask, kernel, iterations = dilations)
                if blursize > 0:    
                    skinMask = cv2.GaussianBlur(skinMask, (blursize, blursize), 0)
                
                self.num_skin_pixels = skinMask.clip(0,1).sum()
                skin = cv2.bitwise_and(frame, frame, mask = skinMask)
                return skin,self.num_skin_pixels
            except:
                pass 
                                   
        return frame,frame.shape[0] * frame.shape[1]
