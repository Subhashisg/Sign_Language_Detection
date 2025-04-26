import cv2
import streamlit as st
import numpy as np
import HandTrackingModule as htm
from pynput.keyboard import Controller
import time
# Helper function to safely get landmark data
def safe_get(lst, idx, dim=3):
    return lst[idx] if len(lst) > idx and len(lst[idx]) >= dim else [0]*dim

# Streamlit UI setup
st.title("Sign Language Recognition")
run = st.checkbox("Start Camera")
FRAME_WINDOW = st.image([])

# Set up camera and hand detector
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = htm.HandDetector(detection_con=0.8)

# Keyboard controller setup
keyboard = Controller()
prev_result = ""
prev_time = 0

while run:
    success, img = cap.read()
    img = detector.find_hands(img)
    posList = detector.find_position(img, draw=False)
    result = ""

    if len(posList) != 0:
        fingers = []
        finger_mcp = [5, 9, 13, 17]
        finger_dip = [6, 10, 14, 18]
        finger_pip = [7, 11, 15, 19]
        finger_tip = [8, 12, 16, 20]

        for i in range(4):
            tip = safe_get(posList, finger_tip[i])
            dip = safe_get(posList, finger_dip[i])
            pip = safe_get(posList, finger_pip[i])
            pinky_tip = safe_get(posList, 16)
            pinky_mcp = safe_get(posList, 20)

            if (tip[1] + 25 < dip[1] and pinky_tip[2] < pinky_mcp[2]):
                fingers.append(0.25)
            elif tip[2] > dip[2]:
                fingers.append(0)
            elif tip[2] < pip[2]:
                fingers.append(1)
            elif tip[1] > pip[1] and tip[1] > dip[1]:
                fingers.append(0.5)

        # Get points
        p = [safe_get(posList, i) for i in range(21)]

        if(p[3][2] > p[4][2]) and (p[3][1] > p[6][1]) and (p[4][2] < p[6][2]) and fingers.count(0) == 4:
            result = "A"
        elif(p[3][1] > p[4][1]) and fingers.count(1) == 4:
            result = "B"
        elif(p[3][1] > p[6][1]) and fingers.count(0.5) >= 1 and (p[4][2] > p[8][2]):
            result = "C"
        elif(len(fingers) > 0 and fingers[0] == 1) and fingers.count(0) == 3 and (p[3][1] > p[4][1]):
            result = "D"
        elif (p[3][1] < p[6][1]) and fingers.count(0) == 4 and p[12][2] < p[4][2]:
            result = "E"
        elif (fingers.count(1) == 3) and (fingers[0] == 0) and (p[3][2] > p[4][2]):
            result = "F"
        elif(len(fingers) > 0 and fingers[0] == 0.25) and fingers.count(0) == 3:
            result = "G"
        elif(len(fingers) > 1 and fingers[0] == 0.25 and fingers[1] == 0.25) and fingers.count(0) == 2:
            result = "H"
        elif (p[4][1] < p[6][1]) and fingers.count(0) == 3 and len(fingers) > 3 and fingers[3] == 1:
            result = "I"
        elif (p[4][1] < p[6][1] and p[4][1] > p[10][1] and fingers.count(1) == 2):
            result = "K"
        elif(len(fingers) > 0 and fingers[0] == 1) and fingers.count(0) == 3 and (p[3][1] < p[4][1]):
            result = "L"
        elif (p[4][1] < p[16][1]) and fingers.count(0) == 4:
            result = "M"
        elif (p[4][1] < p[12][1]) and fingers.count(0) == 4:
            result = "N"
        elif(p[4][2] < p[8][2]) and (p[4][2] < p[12][2]) and (p[4][2] < p[16][2]) and (p[4][2] < p[20][2]):
            result = "O"
        elif(len(fingers) > 2 and fingers[2] == 0) and (p[4][2] < p[12][2]) and (p[4][2] > p[6][2]) and len(fingers) > 3 and fingers[3] == 0:
            result = "P"
        elif(len(fingers) > 3 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and p[8][2] > p[5][2] and p[4][2] < p[1][2]):
            result = "Q"
        elif(p[8][1] < p[12][1]) and (fingers.count(1) == 2) and (p[9][1] > p[4][1]):
            result = "R"
        elif (p[4][1] > p[12][1]) and p[4][2] < p[12][2] and fingers.count(0) == 4:
            result = "S"
        elif (p[4][1] > p[12][1]) and p[4][2] < p[6][2] and fingers.count(0) == 4:
            result = "T"
        elif (p[4][1] < p[6][1] and p[4][1] < p[10][1] and fingers.count(1) == 2 and p[3][2] > p[4][2] and abs(p[8][1] - p[11][1]) <= 50):
            result = "U"
        elif (p[4][1] < p[6][1] and p[4][1] < p[10][1] and fingers.count(1) == 2 and p[3][2] > p[4][2]):
            result = "V"
        elif (p[4][1] < p[6][1] and p[4][1] < p[10][1] and fingers.count(1) == 3):
            result = "W"
        elif(len(fingers) > 0 and fingers[0] == 0.5 and fingers.count(0) == 3 and p[4][1] > p[6][1]):
            result = "X"
        elif(fingers.count(0) == 3) and (p[3][1] < p[4][1]) and len(fingers) > 3 and fingers[3] == 1:
            result = "Y"
        elif (p[4][1] < p[6][1] and p[4][1] < p[10][1] and fingers.count(0) == 2 and p[3][2] > p[4][2]):
            result = "Z"

        # Draw output
        cv2.rectangle(img, (28, 255), (178, 425), (0, 225, 0), cv2.FILLED)
        cv2.putText(img, str(result), (55, 400), cv2.FONT_HERSHEY_COMPLEX, 5, (255, 0, 0), 15)
   
    # Auto-type the recognized letter
        if result and result != prev_result:
            current_time = time.time()
            if current_time - prev_time > 1.0:
                keyboard.type(result)
                prev_result = result
                prev_time = current_time
    # Convert BGR to RGB for Streamlit
    FRAME_WINDOW.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

cap.release()
