import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
import streamlit as st
import os
import cv2
import json

# Khởi tạo Firebase Admin SDK
def init_firebase_local():
    # Tải file JSON chứa chứng chỉ Firebase (Service Account Key)
    cred = credentials.Certificate("firebase/serviceAccountKey.json")
    
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)
        
    # Firestore client
    db = firestore.client()
    return db

# Initialize Firebase Admin SDK
# https://www.youtube.com/watch?v=qAYqdg9UICc&ab_channel=TechnicalRajni
def init_firebase_cloud():
    # Retrieve Firebase credentials from Streamlit secrets and make a copy
    firebase_credentials = dict(st.secrets["FIREBASE_KEY"])
    
    # Fix the private key formatting by replacing '\\n' with '\n'
    firebase_credentials["private_key"] = firebase_credentials["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(firebase_credentials)

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred, {
            'storageBucket': f'{firebase_credentials["project_id"]}.appspot.com'  # Replace with your project ID
        })

    # Return Firestore and Storage clients
    db = firestore.client()
    bucket = storage.bucket()
    return db, bucket

# Hàm lưu thông tin khuôn mặt vào Firestore
def save_face_to_firestore(face_id, image_url=None):
    try:
        # Tham chiếu đến bộ sưu tập 'faces'
        doc_ref = db.collection('faces').document(face_id)
        
        # Lưu thông tin khuôn mặt vào Firestore
        doc_ref.set({
            'face_id': face_id,
            'image_url': image_url if image_url else 'No image',
            'timestamp': datetime.now()
        })
        
        st.success(f"Lưu thành công khuôn mặt: {face_id}")
    except Exception as e:
        st.error(f"Không thể lưu khuôn mặt: {e}")

# Hàm hiển thị các khuôn mặt đã lưu trong Firestore
def display_faces_from_firestore():
    try:
        # Truy vấn tất cả các tài liệu trong bộ sưu tập 'faces'
        docs = db.collection('faces').stream()
        
        # Hiển thị thông tin các khuôn mặt
        if docs:
            for doc in docs:
                st.write(f"ID: {doc.id}, Thời gian: {doc.to_dict().get('timestamp')}, URL ảnh: {doc.to_dict().get('image_url')}")
        else:
            st.info("Chưa có khuôn mặt nào được lưu.")
    except Exception as e:
        st.error(f"Không thể truy xuất dữ liệu từ Firestore: {e}")

# Upload image to Firebase Storage
def upload_image(bucket, img_array, face_id):
    # Convert the OpenCV image to JPEG format
    _, image_encoded = cv2.imencode('.jpg', img_array)
    
    # Save the image in Firebase Storage
    blob = bucket.blob(f"faces/face_{face_id}.jpg")
    
    # Upload the image directly from the encoded bytes
    blob.upload_from_string(image_encoded.tobytes(), content_type="image/jpeg")

    # Get the URL of the uploaded file
    blob.make_public()
    img_url = blob.public_url

    return img_url

# Add face metadata to Firestore
def add_face_data(db, face_id, img_url):
    collection_ref = db.collection('faces')
    face_data = {
        "face_id": face_id,
        "img_url": img_url,
        "timestamp": datetime.now().isoformat()
    }
    collection_ref.add(face_data)
    
