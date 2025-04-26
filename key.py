import cv2
import streamlit as st
import numpy as np
import pyttsx3
import HandTrackingModule as htm
from pynput.keyboard import Controller
import time
import threading

# Helper to safely get landmark
def safe_get(lst, idx, dim=3):
    return lst[idx] if len(lst) > idx and len(lst[idx]) >= dim else [0]*dim

# TTS speaking in background
def speak_letter(letter):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 130)
        engine.say(f"It is {letter}")
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS error: {e}")

# Streamlit UI
st.title("Sign Language Recognition (ASL)")
run = st.checkbox("Start Camera")
FRAME_WINDOW = st.image([])

# Keyboard typing
keyboard = Controller()
prev_result = ""
prev_time = 0

# Camera and Hand Detector
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = htm.HandDetector(detection_confidence=0.8)

while run:
    success, img = cap.read()
    if not success:
        st.error("Failed to capture video.")
        break

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

        p = [safe_get(posList, i) for i in range(21)]

        # Sign detection
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
        # Create a semi-transparent overlay at the top
        overlay = img.copy()

        # Text settings
        font_scale = 3
        font_thickness = 5
        text = str(result)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Get text size
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_width, text_height = text_size

        # Calculate positions
        padding = 20  # padding around the text
        box_width = text_width + 2 * padding
        box_height = text_height + 2 * padding

        top_left = (img.shape[1] // 2 - box_width // 2, 10)
        bottom_right = (img.shape[1] // 2 + box_width // 2, 10 + box_height)

        # Draw semi-transparent box
        cv2.rectangle(overlay, top_left, bottom_right, (0, 0, 0), -1)  # Black filled rectangle
        alpha = 0.4
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Put the text centered in the box
        text_x = img.shape[1] // 2 - text_width // 2
        text_y = 10 + box_height // 2 + text_height // 2 - 5  # Adjust to align vertically

        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

        # Speak and type
        if result and result != prev_result:
            current_time = time.time()
            if current_time - prev_time > 1.0:
                keyboard.type(result)
                threading.Thread(target=speak_letter, args=(result,), daemon=True).start()
                prev_result = result
                prev_time = current_time

    # Streamlit display
    FRAME_WINDOW.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Clean up after Streamlit checkbox is unchecked
cap.release()
cv2.destroyAllWindows()
