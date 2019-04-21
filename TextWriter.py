import cv2
class TextWriter():
    def __init__(self):
        self.line = 1

    def write_text(self,frame,text):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        fontScale              = 0.6
        fontColor              = (255,255,255)
        lineType               = 2
        location = (0,40*self.line)
        cv2.putText(frame,text,location,font,fontScale,fontColor,lineType)
        self.line+=1

    def refresh(self):
        self.line = 1

writer = TextWriter()
def write_text(frame,text):
    writer.write_text(frame,text)
    
def refresh():
    writer.refresh()
    