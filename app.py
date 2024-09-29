import streamlit as st
import cv2
import numpy as np
from datetime import datetime
from utils.face_detection import detect_faces, crop_face
from utils.firebase_utils import init_firebase_cloud, add_face_data, upload_image

# Initialize Firebase
db, bucket = init_firebase_cloud()

st.title("Face Detection App with Streamlit and Firebase")

# Webcam capture using Streamlit
FRAME_WINDOW = st.image([])
run = st.checkbox("Start Webcam")

if run:
    video_capture = cv2.VideoCapture(0)
    face_id_counter = 0  # Unique face ID counter

    while run:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to read from webcam.")
            break

        # Detect faces in the frame
        faces = detect_faces(frame)

        # Loop through detected faces, crop and upload each one
        for (x, y, w, h) in faces:
            face_id = f"{face_id_counter}"
            face_id_counter += 1

            # Crop the face
            cropped_face = crop_face(frame, x, y, w, h)

            # Upload the cropped face image to Firebase
            img_url = upload_image(bucket, cropped_face, face_id)

            # Store face metadata in Firestore
            add_face_data(db, face_id, img_url)

            # Draw a rectangle around the face on the main frame
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Convert the image from BGR (OpenCV format) to RGB (for Streamlit)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    video_capture.release()

else:
    st.write("Click the checkbox to start the webcam.")

