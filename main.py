import cv2
import numpy as np
import time

import Constants
import TargetDetector
import BallDetector



videoWidth = Constants.VIDEO_WIDTH
videoHeight = Constants.VIDEO_HEIGHT

capture = cv2.VideoCapture(0)
# capture = cv2.VideoCapture('img/video_480.mp4')
# capture = cv2.VideoCapture('img/video2_480.mp4')
# capture = cv2.VideoCapture('img/view_480.mp4')
capture.set(3, videoWidth)
capture.set(4, videoHeight)

# debug_image = cv2.imread('img/target1.jpeg')


mode = Constants.MODE_NONE

# cv2.namedWindow("Capture")
# cv2.moveWindow("Capture", 20,20)
cv2.namedWindow("Masked")
cv2.moveWindow("Masked", 1000,20)
cv2.namedWindow("Original")
cv2.moveWindow("Original", 20,500)
cv2.namedWindow("Result")
cv2.moveWindow("Result", 1000,500)


# Call from roborio (actually main loop)
def __stop():
   global mode
   mode = Constants.MODE_NONE

def __detect_targets():
   global mode
   mode = Constants.MODE_DETECT_TARGET

def __detect_balls():
   global mode
   mode = Constants.MODE_DETECT_BALLS





def Init():
   global mode
   mode = Constants.MODE_DETECT_BALLS
   
image = None
success = True

stopped = False
# While loops calls this
def CallPeriodic():
   if mode == Constants.MODE_NONE:
      return

   if not capture.isOpened():
      print("Capture was not opened")
      return
   global success
   global image
   time.sleep(0.01)
   if not stopped:
      success, image = capture.read()
   # image = debug_image
   
   if not success:
      print("Error on CallPeriodic, returned")
      return
   
   if mode == Constants.MODE_DETECT_TARGET:
      TargetDetector.Process(image)
   elif mode == Constants.MODE_DETECT_BALLS:
      BallDetector.Process(image, max_returned_balls=3)


      





if __name__ == "__main__":
   Init()
   i = 0
   capture.set(cv2.CAP_PROP_POS_MSEC, 4000)
   while True:
      CallPeriodic()
      

      # if cv2.waitKey(1) & 0xFF == ord('e'):
      #    stopped = not stopped
      


      # Poll communication with roborio


      # Exit
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break