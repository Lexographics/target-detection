import cv2
import numpy as np

import Constants


############################## Tweaks Window ##############################
def void(x):
   pass

# Opens a new window called Tweak to tweak variables
CAN_TWEAK_VALUES = False
canny_treshold1 = 30
canny_treshold2 = 80
canny_min_area = 10000
if CAN_TWEAK_VALUES:
   cv2.namedWindow("Tweak")
   cv2.moveWindow("Tweak", 650, 800)
   cv2.createTrackbar("canny_treshold1", "Tweak", canny_treshold1,    255, void)
   cv2.createTrackbar("canny_treshold2", "Tweak", canny_treshold2,    255, void)
   cv2.createTrackbar("lower", "Tweak", 110,    255, void)
   cv2.createTrackbar("upper", "Tweak", 255,    255, void)
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



# Returns left/right -> distance between center of camera and target center -- left/right == 0 means target is perfectly centered
def Process(image):
   original_image = image.copy()
   hsv_original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

   bgr_img = original_image.copy()
   hsv_img = hsv_original_image.copy()

   # Gaussian blur

# *in BGR   
   lower_green = np.array([0 , cv2.getTrackbarPos("lower", "Tweak"),  0])
   upper_green = np.array([180, cv2.getTrackbarPos("upper", "Tweak"),100])

# *in HSV
   lower_green_hsv = np.array([cv2.getTrackbarPos("lower", "Tweak") , 0,  0])
   upper_green_hsv = np.array([cv2.getTrackbarPos("upper", "Tweak"), 255,  255])


   mask = cv2.inRange(bgr_img, lower_green, upper_green)
   # Remove noise
   kernel =  np.ones((5,5),np.uint8)
   mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

   # Apply mask
   res = cv2.bitwise_and(bgr_img, bgr_img, mask= mask)
   # Discard small pieces && noises
   res = cv2.dilate(res, np.ones((3, 3)), iterations=1)

   res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

   # Find contours
   contours, hierarchy = cv2.findContours(res_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   i = 0
   max_contour_area = 0
   biggest_contour = None
   # draw contours
   for cnt in contours:
      # Test for area
      area = cv2.contourArea(cnt)
      area_limit = getMinArea()
      # if area < area_limit: continue
      if area > max_contour_area:
         max_contour_area = area
         biggest_contour = cnt

      # Test for corner count
      par1 = cv2.arcLength(cnt, True)
      corners = cv2.approxPolyDP(cnt, 0.02*par1, True)

      x, y, w, h = cv2.boundingRect(corners)

      i += 1
      for corner in corners:
         # Target cannot have more than 10 points
         if len(corner) > 10: continue
         
         for c in corner:
            cv2.rectangle(bgr_img, [c[0]-5, c[1]-5], [c[0]+5, c[1]+5], (200, 100, min(i*20, 255)), 2)
         

         total_distance = 0
         point_count = len(corners)
         
         average_distance = 0
         max_distance = 0
         for c in corner:
            dist = np.sqrt( (c[0] * c[0]) + (c[1] * c[1]) )
            if dist > max_distance:
               max_distance = dist
               
            total_distance += dist

         average_distance = total_distance / point_count

         # print(f"avg({average_distance}) : max({max_distance})")
         
         if max_distance < average_distance * 4: continue
         

      


      
      cv2.rectangle(bgr_img, (x, y), (x+w, y+h), (0, 255, 0), 1)
      cv2.putText(bgr_img, f"Corner Count: {len(corners)}", (x+(w*0)+10, y-20), cv2.FONT_HERSHEY_TRIPLEX, min(.7, area*0.01), (0, 0, 255), 2)

   
   left_right = 0
   # Got biggest contour
   if max_contour_area > 0:
      cv2.drawContours(bgr_img,biggest_contour,0,(0,0,255),2)

      # Test for corner count
      par1 = cv2.arcLength(biggest_contour, True)
      corners = cv2.approxPolyDP(biggest_contour, 0.02*par1, True)

      x, y, w, h = cv2.boundingRect(corners)

      cv2.rectangle(bgr_img, (x, y), (x+w, y+h), (100, 255, 255), 4)
      
      
      center_point = [x+int(w/2), y+int(h/2)]

      cv2.rectangle(bgr_img, [center_point[0]-5, center_point[1]-5], [center_point[0]+5, center_point[1]+5], (255, 255, 255), 4)


      screen_center_point = Constants.video_width / 2
      left_right = center_point[0] - screen_center_point
      


 
   cv2.imshow('Mask'   , mask)
   cv2.imshow('Result' , res)
   cv2.imshow("Capture", bgr_img)
   cv2.imshow("Original", original_image)

   return left_right