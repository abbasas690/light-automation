import cv2

class Cam:
    def __init__(self,address,width=1280,height=720):
        self.address = address 
        self.width = width
        self.height = height

    def setconfig(self):
        video = cv2.VideoCapture(self.address)
        video.set(3,self.width)
        video.set(4,self.height)
        return video

#         
#     def show(self):
#         video = self.setconfig()
#         while True:
#             check , frame = self.frame(video)
#             cv2.imshow("hello",frame)
#             key=cv2.waitKey(1)
#             
#             if key==ord('q'):
#                 break
#         video.release()
#         cv2.destroyAllWindows

# if __name__ == "__main__":
#     cam = Cam("http://192.168.226.145:8080/video")
#     cam.show()
