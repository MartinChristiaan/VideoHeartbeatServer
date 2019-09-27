from server import create_server


import logging
log = logging.getLogger('werkzeug')
           
        
audio_path = librosa.util.example_audio_file()
y, sr = librosa.load("/home/martin/Downloads/Darkside.wav")
y_harmonic, y_percussive = librosa.effects.hpss(y)
C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, bins_per_octave=36)
onset = librosa.onset.onset_detect(y,sr)
#%%




from scipy import signal
t_onset = onset*(len(y)/sr)/C.shape[1]
f_onset = C[:,onset]







#%%
import time
class Main:
    def __init__(self,t_onset):
        self.t_onset = t_onset
        self.f_onset = np.ones_like(t_onset)
#        self.percent = 0
#        self.idx = np.arange(C.shape[0])
#        self.onsets = beatViz
#        self.chroma = C[:,0]
#        self.curbeat = 0
#
#       # synchronizes with song in browser 
#    def update_chroma(self):
#        new_idx =  int(self.percent * C.shape[1])
#        self.chroma = C[:,new_idx]
#        self.curbeat = self.onsets[new_idx]
#        song_duration = len(y)/sr
#        dt = song_duration/C.shape[1]
#        for idx in range(new_idx,C.shape[1]):
#            time.sleep(dt)
#            self.chroma = C[:,idx]
#            self.curbeat = self.onsets[idx]
#        
#    def main(self):
#        pass

main = Main(t_onset)
if __name__ == '__main__':
    app = create_server([main])
    app.run(threaded = True)



