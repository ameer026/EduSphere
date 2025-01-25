import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide")

# Initialize session state for camera control and output text
if 'run' not in st.session_state:
    st.session_state.run = False
if 'last_output' not in st.session_state:
    st.session_state.last_output = ""

col1, col2 = st.columns([2, 1])
with col1:
    if st.button('Start Camera'):
        st.session_state.run = True
    if st.button('Stop Camera'):
        st.session_state.run = False
    
    FRAME_WINDOW = st.image([])

with col2:
    output_text_area = st.title("Answer")
    output_text_area = st.subheader("")

genai.configure(api_key="AIzaSyByIY4yY7eCHdxsDRmcE_Z3B28aPNs0Cag")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

def getHandInfo(img):
    hands, img = detector.findHands(img, draw=False, flipType=True)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    return None

def draw(info, prev_pos, canvas):
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lmList[8][0:2]
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas, current_pos, prev_pos, (255, 0, 255), 10)
    elif fingers == [1, 0, 0, 0, 0]:
        canvas = np.zeros_like(img)
    return current_pos, canvas

def sendToAI(model, canvas, fingers):
    if fingers == [0, 1, 1, 1, 1]:
        try:
            pil_image = Image.fromarray(canvas)
            response = model.generate_content(["Solve this math problem", pil_image])
            return response.text
        except Exception as e:
            st.error(f"AI Generation Error: {e}")
    return None

prev_pos = None
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

while True:
    if st.session_state.run:
        success, img = cap.read()
        img = cv2.flip(img, flipCode=1)

        info = getHandInfo(img)
        if info:
            fingers,lmList = info
            prev_pos, canvas = draw(info, prev_pos, canvas)
            output_text = sendToAI(model, canvas, fingers)

            # Check for new output to avoid repetition
            if output_text and output_text != st.session_state.last_output:
                st.session_state.last_output = output_text
                st.subheader(output_text)

        image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
        image_combined_rgb = cv2.cvtColor(image_combined, cv2.COLOR_BGR2RGB)
        
        FRAME_WINDOW.image(image_combined_rgb)

    cv2.waitKey(1)
