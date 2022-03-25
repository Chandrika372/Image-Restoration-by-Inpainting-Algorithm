#Code for image restoration using OpenCVC FMM and NS algorithm
import cv2 as cv
import sys
import numpy as np

class sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt=None
        self.windowname=windowname
        self.dests=dests
        self.colors_func=colors_func
        self.dirty=False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)
        
    def show(self):
        cv.imshow(self.windowname, self.dests[0])
        cv.imshow(self.windowname+": Mask",self.dests[1])
        
    def on_mouse(self, event, x, y, flags, param):
        pt=(x,y)
        if event==cv.EVENT_LBUTTONDOWN:
            self.prev_pt=pt
        elif event==cv.EVENT_LBUTTONUP:
            self.prev_pt=None
        if self.prev_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv.line(dst, self.prev_pt, pt, color, 5)
            self.dirty= True
            self.prev_pt= pt
            self.show()
                
        
def main():
    print("Usage:Python Inpaint")
    print("Keys: ")
    print("t - inpaint using FMM")
    print("n - inpaint using NS technique")
    print("r- reset the inpaint mask")
    print("ESC - exit")
    #read the image
    #img=cv.imread("C:/Users/Chandrika PC/OneDrive/Pictures/Saved Pictures/112f654e93386ecffebb72bb82f0f691.jpg",cv.IMREAD_COLOR)
    img=cv.imread("C:/Users/Chandrika PC/Downloads/finedetails.jpg",cv.IMREAD_COLOR)
    if img is None:
        print("Failed to load image file: {}".format(img))
        return 
  
    img_mask=img.copy()
    
    inpaintMask=np.zeros(img.shape[:2],np.uint8)
    sketch = sketcher('image',[img_mask,inpaintMask], lambda :((255,255,225), 255))
    while True:
        ch=cv.waitKey(0)
        
        if ch== 27:
            break
        if ch== ord('t'):
            res=cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv.INPAINT_TELEA)
            cv.imshow("Output using FMM",res)
        if ch== ord('n'):
            res=cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv.INPAINT_NS)
            cv.imshow("Output using NS",res)
        if ch== ord('r'):
            img_mask[:]=img
            inpaintMask[:]=0
            sketch.show()
        print("Completed")
        
    
        
    
if __name__=='__main__':
        main()
        cv.destroyAllWindows()
