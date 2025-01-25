import numpy as np
import cv2

img = cv2.resize(cv2.imread('assets/soccer_practice.jpg',0),(0,0),fx=0.5,fy=0.5)
template = cv2.resize(cv2.imread('assets/shoe.PNG',0),(0,0),fx=0.5,fy=0.5)
#img2 = img.copy()
h,w = template.shape
#(height, width, channels)

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR,cv2.TM_CCORR_NORMED,cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]

for method in methods:
    img2 = img.copy()

    result = cv2.matchTemplate(img2,template, method)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
    #print(min_loc,max_loc)
    if method in [cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    bt_r =(location[0]+w, location[1]+h)
    cv2.rectangle(img2,location,bt_r,255,5)
    cv2.imshow('Match',img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
