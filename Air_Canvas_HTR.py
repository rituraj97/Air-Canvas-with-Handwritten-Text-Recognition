import numpy as np
import cv2
from PIL import Image 
from collections import deque
import os
from HTR_System import HTR_System_Method

def AirCanvas():
    bpoints = [deque(maxlen=1024)]
    blue_index = 0

    #kernel to be used for dilation purposes
    kernel = np.ones((5,5), np.uint8)
    colors = [(255,0,0)]
    colorIndex = 0



    #Canvas Setup
    paintWindow = np.zeros((471,636,3)) + 255
    ##paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), (0,0,0), 2)
    cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

    #loading the default webcam of your pc 
    cap = cv2.VideoCapture(0)

    while(True):
        #Reading the frame from the camera
        ret,frame = cap.read()
        #flipping the frame
        frame = cv2.flip(frame,1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        Upper_hsv = np.array([153, 255, 255])
        Lower_hsv = np.array([64, 72, 49])

        #Live Frame
        frame = cv2.rectangle(frame, (275,1), (375,65), (122,122,122), -1)
        cv2.putText(frame, "CLEAR ALL", (284,33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA )

        #identifying the pointer by making mask
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv2.erode(Mask, kernel, iterations=1)
        Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
        Mask = cv2.dilate(Mask, kernel, iterations=1)

        #find contours for the pointer
        cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        center = None

        # If the contours are formed
        if len(cnts) > 0:
            # sorting the contours to find biggest 
            cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
            # Get the radius of the enclosing circle around the found contour
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # Calculating the center of the detected contour
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Now checking if the user wants to click on any button above the screen 
            if center[1] <= 65:
                if 275 <= center[0] <= 375:
                    bpoints = [deque(maxlen=512)]
                    blue_index = 0
                    paintWindow[67:,:,:] = 255
                else: 
                    colorIndex = 0
            else:
                if colorIndex==0:
                    bpoints[blue_index].appendleft(center)

        #Append the next deques when nothing is detected to avoid messing up
        else:
            bpoints.append(deque(maxlen=512))
            blue_index+=1
        
        #Draw lines on Canvas and Frame
        points = [bpoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k-1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k-1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k-1], points[i][j][k], colors[i], 2)

        #show windows
        cv2.imshow("Tracking Camera Window", frame)
        cv2.imshow("Paint", paintWindow)
        #cv2.imshow("Mask", Mask)

        #if 's' is pressed save the image
        if cv2.waitKey(1) & 0xFF == ord("s"):
            status = cv2.imwrite('--PATH TO PROJECT DIRECTORY--/handwriting.png', paintWindow)  
            print("Image written to file-system : ",status)
            # val = os.system('python C:/Users/saura/OneDrive/Desktop/Air-Canvas-project/HTR_System.py')
            val = HTR_System_Method()
            break

        # If the 'q' key is pressed then stop the application 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Exit")
            break

    # Release the camera and all resources
    cap.release()
    cv2.destroyAllWindows()
    return val

