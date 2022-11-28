import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import time

"""
Inputs:
    - video stream of white background with coloured mnms on it

Outputs:
    - the X, Y position of 1 of the mnms for the robot to go to

Method:
    - Iterate through the different colours of mnms and locate them
    - Write the location of 1 of the mnms to a text file, ues the  
    rotation parameter to distinguish colour
"""

cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )

mnms = cv2.imread("m&m.png")

GREEN_COLOUR = [0, 255, 0]
GREEN_ANGLE = 120

YELLOW_COLOUR = [0, 255, 255]
YELLOW_ANGLE = 60

ORANGE_COLOUR = [0, 110, 215]
ORANGE_ANGLE = 30

while True:
    
    # _, frame = cap.read()
    ret, frame = cap.read()
    # print(ret)

    blur = cv2.GaussianBlur(frame, (9,9), 0)
    hsv_frame = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask_dict = {}

    # low_red = np.array([0, 46, 40])
    # high_red = np.array([4, 255, 255])
    # red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    # mask_dict['Red'] = red_mask
    # cv2.imshow("Red", red_mask)

    low_green = np.array([55, 46, 40])
    high_green = np.array([65, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    mask_dict['Green'] = [green_mask, GREEN_COLOUR, GREEN_ANGLE]
    # cv2.imshow("Green", green_mask)

    low_yellow = np.array([20, 70, 70])
    high_yellow = np.array([26, 255, 255])
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
    mask_dict['Yellow'] = [yellow_mask, YELLOW_COLOUR, YELLOW_ANGLE]
    # cv2.imshow("Yellow", yellow_mask)

    # low_purple = np.array([0, 0, 0])
    # high_purple = np.array([179, 110, 80])
    # purple_mask = cv2.inRange(hsv_frame, low_purple, high_purple)
    # mask_dict['Purple'] = purple_mask
    # # cv2.imshow("Purple", purple_mask)

    low_orange = np.array([5, 40, 40])
    high_orange = np.array([15, 255, 255])
    orange_mask = cv2.inRange(hsv_frame, low_orange, high_orange)
    mask_dict['Orange'] = [orange_mask, ORANGE_COLOUR, ORANGE_ANGLE]
    # cv2.imshow("Orange", orange_mask)
    
    for key in mask_dict:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
        mask_dict[key][0] = cv2.morphologyEx(mask_dict[key][0], cv2.MORPH_OPEN, kernel)
        # mask_dict[key] = cv2.morphologyEx(mask_dict[key], cv2.MORPH_CLOSE, kernel)
        cv2.imshow(key, mask_dict[key][0])
        contours, _ = cv2.findContours(mask_dict[key][0], cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # print(area)
            if area > 800:
                (x,y),radius = cv2.minEnclosingCircle(cnt)
                center = (int(x),int(y))
                radius = int(radius)

                cv2.circle(frame, center,radius,mask_dict[key][1],2)
                if center[0] > 0 and center[1] > 0:
                    if center[0] < width and center[1] < height:
                        f = open("test.txt", 'w')
                        f.write(str(center[0]) + ',' + str(center[1]) + ',' + str(mask_dict[key][2]))
                        f.close()

    # # cv2.imshow("HSV", hsv_frame)
    # # cv2.imshow("Mask", mask)
    # # cv2.imshow("mnms", colours)

    cv2.imshow("Frame", frame)
    # time.sleep(0.2)
    #     ellipse = cv2.fitCircle(cnt)
    #     centerX = ellipse[0][0]
    #     centerY = ellipse[0][1]
    #     positions.append((centerX, centerY))
    # print(positions)
    # positions = find_mnms(mask, frame)

    # axis2 = fig.add_subplot(2,1,1)
    # axis2.imshow(hsv_mnms)
    # plt.show()
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
