# -*- coding: utf-8 -*-


import numpy as np
import scipy.io as sio
from scipy import signal
from rppgsensor import PPGSensor
# Params
R = 0
G = 1
B = 2

class Proccessor():
    def __init__(self,sensor : PPGSensor,framecapture):
        self.fftlength = 300
        self.fs = framecapture.fs
        self.sensor = sensor
        self.x_stride_method = []
        self.normalized_amplitude = []
        self.enough_samples = False

class ChrominanceExtracter(Proccessor):
    def extract_pulse(self):
        rPPG = self.sensor.rppg
        fs = self.fs
        fftlength = self.fftlength 
        if(rPPG.shape[1] < fftlength):
            return 
        else:
            self.enough_samples = True

        fft_roi = range(int(fftlength/2+1)) # We only care about this part of the fft because it is symmetric anyway
        bpf_div= 60 * fs / 2
        b_BPF40220,a_BPF40220 = signal.butter(10, ([40/bpf_div, 220/bpf_div]),  'bandpass') 
        
        col_c = np.zeros((3,fftlength))
        skin_vec = [1,0.66667,0.5]
        for col in [R,G,B]:
            col_stride = rPPG[col,-fftlength:]# select last samples
            y_ACDC = signal.detrend(col_stride/np.mean(col_stride))
            col_c[col] = y_ACDC * skin_vec[col]
        X_chrom = col_c[R]-col_c[G]
        Y_chrom = col_c[R] + col_c[G] - 2* col_c[B]
        Xf = signal.filtfilt(b_BPF40220,a_BPF40220,X_chrom) # Applies band pass filter
        Yf = signal.filtfilt(b_BPF40220,a_BPF40220,Y_chrom)
        Nx = np.std(Xf)
        Ny = np.std(Yf)
        alpha_CHROM = Nx/Ny
        self.x_stride_method = Xf- alpha_CHROM*Yf
        STFT = np.fft.fft(self.x_stride_method,fftlength)[fft_roi]
        self.normalized_amplitude = np.abs(STFT)/np.max(np.abs(STFT))


rPPG = sio.loadmat('mixed_motion_tracker.mat')['rPPG']

fs = 20
fftlength = 300

fft_roi = range(int(fftlength/2+1)) # We only care about this part of the fft because it is symmetric anyway
bpf_div= 60 * fs / 2
b_BPF40220,a_BPF40220 = signal.butter(10, ([40/bpf_div, 220/bpf_div]),  'bandpass') 

col_c = np.zeros((3,fftlength))


ii = 0
stride =np.arange(-np.fix(fftlength/2),np.fix(fftlength/2),1,dtype = int) + T[ii]
col_c = np.zeros((3,fftlength))
for col in [R,G,B]:
    col_stride = rPPG[col,stride]# select last samples
    y_ACDC = signal.detrend(col_stride/np.mean(col_stride))
    col_c[col,stride] = signal.filtfilt(b_BPF40220,a_BPF40220,y_ACDC)
pbv = np.array([0.316168778558440,0.441909354756743,0.272299180445891])
S = np.matmul(col_c ,np.transpose(col_c))
W = np.linalg.solve(S,pbv)
x_stride_method = np.matmul(col_c.T,W)/(np.matmul(pbv.T,W)) 
STFT = np.fft.fft(x_stride_method,fftlength)[fft_roi]
normalized_amplitude = np.abs(STFT)/np.max(np.abs(STFT))

import matplotlib.pyplot as plt
plt.plot(normalized_amplitude)