import cv2
import numpy as np

import Constants


############################## Tweaks Window ##############################
def void(x):
   pass

# Opens a new window called Tweak to tweak variables
CAN_TWEAK_VALUES = True
canny_treshold1 = 30
canny_treshold2 = 80
canny_min_area = 100
if CAN_TWEAK_VALUES:
   cv2.namedWindow("Tweak")
   cv2.moveWindow("Tweak", 650, 800)
   cv2.createTrackbar("canny_treshold1", "Tweak", canny_treshold1,    255, void)
   cv2.createTrackbar("canny_treshold2", "Tweak", canny_treshold2,    255, void)
   cv2.createTrackbar("lower_h", "Tweak",   17,    255, void)
   cv2.createTrackbar("upper_h", "Tweak",   33,    255, void)
   cv2.createTrackbar("lower_s", "Tweak",   80,    255, void)
   cv2.createTrackbar("upper_s", "Tweak",  255,    255, void)
   cv2.createTrackbar("lower_v", "Tweak",  143,    255, void)
   cv2.createTrackbar("upper_v", "Tweak",  255,    255, void)
   cv2.createTrackbar("crop"   , "Tweak",  240,    480, void)
   cv2.createTrackbar("canny_min_area" , "Tweak", canny_min_area , 100000, void)

# Returns Two limit values for canny edge detector
def getLimits():
   if CAN_TWEAK_VALUES:
      limit1 = cv2.getTrackbarPos("canny_treshold1", "Tweak")
      limit2 = cv2.getTrackbarPos("canny_treshold2", "Tweak")
   return limit1, limit2
def getMinArea():
   if CAN_TWEAK_VALUES:
      min_area = cv2.getTrackbarPos("canny_min_area", "Tweak")
   return min_area
###########################################################################





# [ 
#     [left/right, Radius],
#     [left/right, Radius],
#     [left/right, Radius],
# ]
def Process(_image, max_returned_balls=3):
   image = _image.copy()
   img = image.copy()
   # only get lower half part of screen
   img = img[cv2.getTrackbarPos("crop", "Tweak"):480, 0:850]

   #hsv_image = cv2.GaussianBlur(img, (11, 11), 0)
   hsv_image = cv2.GaussianBlur(img, (0, 0), sigmaX=3, sigmaY=3)
   # blur = cv2.GaussianBlur(gray, (0,0), sigmaX=33, sigmaY=33)
   hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)

   # *in HSV
   lower_yellow_hsv = np.array([cv2.getTrackbarPos("lower_h", "Tweak"), cv2.getTrackbarPos("lower_s", "Tweak"),  cv2.getTrackbarPos("lower_v", "Tweak")])
   upper_yellow_hsv = np.array([cv2.getTrackbarPos("upper_h", "Tweak"), cv2.getTrackbarPos("upper_s", "Tweak"),  cv2.getTrackbarPos("upper_v", "Tweak")])


   mask = cv2.inRange(hsv_image, lower_yellow_hsv, upper_yellow_hsv)
   mask = cv2.erode(mask, None, iterations=2)
   mask = cv2.dilate(mask, None, iterations=2)
   res = cv2.bitwise_and(hsv_image, hsv_image, mask= mask)

   

   contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   max_contour = None
   #if len(contours) > 0:
   
   for contour in contours:
      if len(contour) < 5: continue
      # max_contour = contours[0]
      
      #for contour in contours:
      #   area = cv2.contourArea(contour)
      #   if area > cv2.contourArea(max_contour):
      #      max_contour = contour   
      #   pass
      
      # contour = max(contours, key=cv2.contourArea)
      (x, y), (major, minor), angle = cv2.fitEllipse(contour)
      radius = int((major + major) /4.0)


      ((x, y), radius) = cv2.minEnclosingCircle(contour)
      if radius > 0:
         cv2.putText(image, f"radius: {round(radius, 2)}", (int(x-(radius*2)), int(y-30+cv2.getTrackbarPos("crop", "Tweak"))), cv2.FONT_HERSHEY_COMPLEX, min(radius*0.02, 0.5), (192, 161, 243), 2)
         cv2.circle(image, (int(x), int(y+cv2.getTrackbarPos("crop", "Tweak"))), int(radius), (90, 255, 90), 1)
         cv2.rectangle(image, [int(x-radius), int(y-radius+cv2.getTrackbarPos("crop", "Tweak"))], [int(x+radius), int(y+radius+cv2.getTrackbarPos("crop", "Tweak"))], (0, 60, 255), 2)
            
      


   cv2.imshow("Original", image)
   cv2.imshow("Result", hsv_image)
   cv2.imshow("Mask", mask)
   cv2.imshow("Masked", cv2.cvtColor(res, cv2.COLOR_HSV2BGR))

   return