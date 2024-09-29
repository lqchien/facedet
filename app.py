import streamlit as st
import cv2
from PIL import Image
import numpy as np
from datetime import datetime
from utils.face_detection import detect_faces, crop_face
from utils.firebase_utils import init_firebase_cloud, add_face_data, upload_image

# Initialize Firebase
db, bucket = init_firebase_cloud()

# Streamlit App Title
st.title("Face Detection App with Firebase")

face_id_counter = 0

# Upload Image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

# If an image is uploaded
if uploaded_file is not None:
    # Convert the uploaded image to an OpenCV image
    image = np.array(Image.open(uploaded_file))

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Add a "Detect" button
    if st.button("Detect"):

        # Step 2: Detect Faces in the Uploaded Image
        faces = detect_faces(image)
        
        # Loop through detected faces, crop and upload each one
        for (x, y, w, h) in faces:
            face_id = f"{face_id_counter}"
            face_id_counter += 1

            # Crop the face
            cropped_face = crop_face(image, x, y, w, h)

#            # Upload the cropped face image to Firebase
#            img_url = upload_image(bucket, cropped_face, face_id)

#            # Store face metadata in Firestore
#            add_face_data(db, face_id, img_url)

            # Draw a rectangle around the face on the main image
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Convert the image from BGR (OpenCV format) to RGB (for Streamlit)
#        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#        FRAME_WINDOW.image(frame)
        st.image(image, caption="Image with Detected Faces", use_column_width=True)

    else:
        st.warning("No faces detected.")

