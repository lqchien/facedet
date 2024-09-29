import cv2

# Load mô hình Haarcascade để phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Hàm phát hiện khuôn mặt
def detect_faces(frame):
    # Chuyển đổi hình ảnh sang grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Phát hiện khuôn mặt trong ảnh grayscale
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

#    # Vẽ hình chữ nhật xung quanh mỗi khuôn mặt được phát hiện
#    for (x, y, w, h) in faces:
#        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return faces

def crop_face(frame, x, y, w, h):
    # Crop the face from the frame using the coordinates
    return frame[y:y+h, x:x+w]
