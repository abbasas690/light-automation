from src.detect import Detect
from src.cam import Cam
import cv2
import pyfirmata

CAM_LINK=''  #cam link should be provided else default video will be played
             #eg:'http://100.81.130.47:8080/video'
BOARD_PORT='/dev/ttyACM0' #Arduino board port
PIN=13    #led digital pip 
FRAME_WIDTH=600   #width of the frame  ie) output window width
FRAME_HEIGHT=420  #height of the frame  ie) output window height 
LIST_OF_OBJECT_TO_DETECT=[2] # list of object numbers from the  below name.
                             #give the corresponding numbers to turn on led for that object 
MODEL='n' #for more accurate dectection use 
          #n - nano, s - small, m - medium, l - large, x - huge. 
          #caution: the more you go need more process power 

RES_DIR='./res'
CAM_OR_FILE=CAM_LINK or RES_DIR+'/sample.mp4'    
MODEL_WEIGHT=RES_DIR+'/weight/'+'yolov8'+MODEL+'.pt'

name={0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck',
 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird',
 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe',
 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard',
 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant',
 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave',
 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier',
 79: 'toothbrush'}



def light_on():
    STATE_OF_LED=True
    print("on")
    borad.digital[PIN].write(1)

def light_off():
    borad.digital[PIN].write(0)
    STATE_OF_LED=False
    print("off")



def main():
    while True:
        re,frame=video.read()
        if not re:
            continue
        results = model.predict(frame)
        for result in results:
              for box in result.boxes:
                 x1,y1,w,h,conf,cls=model.calculate_box(box)
                 className=results[0].names
                 name=className[cls]
                 if conf > 70: 
                   model.draw_box(x1,y1,w,h,conf,name,frame)
                   model.label.append(className[cls])
                   print("lable has more confiden: ",model.label)
              on_or_off =any([i in TURN_ON_LIST for i in model.label])
              model.label.clear()
              if on_or_off :
                 if STATE_OF_LED :
                     pass
                 else:
                     light_on()
              else:
                  light_off()
              cv2.imshow("object detection",frame)
              key=cv2.waitKey(1)
              if key == ord('q'):
                  video.release()
                  cv2.destroyAllWindows()
                  return 1

if __name__ == "__main__":

    TURN_ON_LIST = [name[i] for i in LIST_OF_OBJECT_TO_DETECT]
    STATE_OF_LED=False
    borad = pyfirmata.Arduino(BOARD_PORT)
    light_off()
    model = Detect(MODEL_WEIGHT)
    model.fit()
    cam = Cam(CAM_OR_FILE,width=FRAME_WIDTH,height=FRAME_HEIGHT)
    video = cam.setconfig()
    main()
    light_off()


