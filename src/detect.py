# from  cam import Cam
from ultralytics import YOLO
import cvzone
import math
import cv2


class Detect:
   def __init__(self, weight):
     self.weight=weight
     self.model=None
     self.label=list()

   def fit(self):
     self.model=YOLO(self.weight)
   
   def predict(self,img):
      results = self.model.predict(img)
      return results

   def calculate_box(self,box):
     x1, y1, x2, y2 = [int(i) for i in box.xyxy[0].tolist()]
     w, h = x2-x1,y2-y1
     cls = int(box.cls[0])
     conf = math.ceil((box.conf[0]*100))
     return x1,y1,w,h,conf,cls

   def draw_box(self,x1,y1,w,h,conf,cls,img):
     cvzone.cornerRect(img,(x1,y1,w,h),l=15)
     cvzone.putTextRect(img,f'{cls} {conf}%',(max(0,x1),max(35,y1)),scale=0.9, thickness=1,offset=3)

