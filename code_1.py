import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
import pyautogui as autopy

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities

WIDTH = 1980
HEIGHT =1080
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    # image.flags.writeable = True                   # Image is now writeable 
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return results
def quad_est(x,y):
    #estimator for parsing and generating curve for 3 points
    polyfit = np.polynomial().fit(x,y,2)
    A, B, C = polyfit.coef
    return A,B,C
def quad_calc(A,B,C,x):
    return A*x**2+B*x+C
cap = cv2.VideoCapture(0)
# Set mediapipe model 
autopy.FAILSAFE = False
ismousedown =  False
mousemotion = []
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        # Read feed
        ret, frame = cap.read()

        # Make detections
        results = mediapipe_detection(frame, holistic)
        # Show to screen
        if results.right_hand_landmarks:
            
            # h, w, _ = image.shape
            xi = results.right_hand_landmarks.landmark[8].x
            yi = results.right_hand_landmarks.landmark[8].y
            xt = results.right_hand_landmarks.landmark[4].x
            yt = results.right_hand_landmarks.landmark[4].y
            xl = results.right_hand_landmarks.landmark[20].x
            yl = results.right_hand_landmarks.landmark[20].y
            # xix = int(w*xi)
            # yix = int(h*yi)
            # xtx = int(w*xt)
            # ytx = int(h*yt)
            autopy.moveTo((1-1.20*xi)*WIDTH,(yi)*HEIGHT)
            
            if ((xl-xt)**2+(yl-yt)**2)**0.5 < 0.04:
                print("click hua @",xi,yi,((xl-xt)**2+(yl-yt)**2)**0.5)
                if not ismousedown:
                    autopy.mouseDown(button='left')
                    ismousedown = True
            else:
                if ismousedown:
                    autopy.mouseUp(button='left')
                    ismousedown = False
        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()