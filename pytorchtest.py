# -*- coding: utf-8 -*-
import torch
import time
import numpy as np


model=torch.load('modelfile.txt')
 
import cv2 


def classifySkin(frame)
    imre = im.reshape(im.shape[0] * im.shape[1],3) 
    imre = torch.tensor(imre, device=device,dtype = torch.float)
    yim = model(imre)
    newim = torch.tensor(np.zeros((im.shape[0] * im.shape[1],3)), device=device,dtype = torch.float)
    for col in [0,1,2]:
        newim[:,col] = yim[:,0] * imre[:,col]
    newimval =np.array(newim.data.tolist(),dtype=np.uint8).reshape(im.shape[0],im.shape[1],3)
    
    return newimval

