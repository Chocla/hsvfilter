import numpy as np
import cv2

def getBiggestContour(contours):
    maxArea = 0
    maxIndex = 0
    i = 0
    while i < len(contours):
        tmpArea = cv2.contourArea(contours[i])
        if tmpArea > maxArea:
            maxArea = tmpArea
            maxIndex = i
        i += 1
    return contours[maxIndex]

yellow_low = np.array([20,100,100])
yellow_high = np.array([30,255,255])

orange_low = np.array([5,100,100])
orange_high = np.array([25,255,255])

frame = cv2.imread('orange2.jpg')
frame_HSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
frame_threshed = cv2.inRange(frame_HSV, orange_low,orange_high)
cv2.imshow("orange",frame_threshed)

c, h = cv2.findContours(frame_threshed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contour = getBiggestContour(c)
x,y,w,h = cv2.boundingRect(contour)
cv2.rectangle(frame, (x,y) , (x+w,y+h), (0,255,0))
cv2.arrowedLine(frame, (50,50),(100,100), (0,255,0), 5)
# cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
cv2.imshow("contoured",frame)
# im = cv2.imread('rubiks-cube.jpg')
# hsv_im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv_im,yellow_low,yellow_high)
# hsv_im[mask > 0] = ([25,255,255])
# back = cv2.cvtColor(hsv_im,cv2.COLOR_HSV2BGR)
# gray = cv2.cvtColor(back,cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(gray,150,255,0)

# cv2.imshow('a',hsv_im)
# cv2.imshow('original',im)
# cv2.imshow('filtered',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()