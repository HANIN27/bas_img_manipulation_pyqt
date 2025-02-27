import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

# Load OpenCV's pre-trained deep learning models
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
AGE_MODEL = r"C:\Users\Dr. HOMEIRA NISHAT\Desktop\pyqt sam\models\age_deploy.prototxt"
GENDER_MODEL = r"C:\Users\Dr. HOMEIRA NISHAT\Desktop\pyqt sam\models\gender_deploy.prototxt"
PROTOTXT = r"C:\Users\Dr. HOMEIRA NISHAT\Desktop\pyqt sam\models\deploy.prototxt"


# Load the models
age_net = cv2.dnn.readNetFromCaffe(PROTOTXT, AGE_MODEL)
gender_net = cv2.dnn.readNetFromCaffe(PROTOTXT, GENDER_MODEL)

# Age & Gender categories
AGE_LABELS = ["(0-2)", "(4-6)", "(8-12)", "(15-20)", "(25-32)", "(38-43)", "(48-53)", "(60-100)"]
GENDER_LABELS = ["Male", "Female"]

# Face Database (Preload known faces)
KNOWN_FACES = {
    "elon.jpg": "Elon Musk",
    "steve.jpg": "Steve Jobs"
}

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition & Age/Gender Detection")
        self.setGeometry(500, 200, 800, 600)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        self.button_load = QPushButton("Load Image", self)
        self.button_detect = QPushButton("Detect Faces", self)
        self.button_webcam = QPushButton("Start Webcam", self)
        self.button_stop_webcam = QPushButton("Stop Webcam", self)

        self.button_load.clicked.connect(self.load_image)
        self.button_detect.clicked.connect(self.detect_faces)
        self.button_webcam.clicked.connect(self.start_webcam)
        self.button_stop_webcam.clicked.connect(self.stop_webcam)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_load)
        layout.addWidget(self.button_detect)
        layout.addWidget(self.button_webcam)
        layout.addWidget(self.button_stop_webcam)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = None
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.detect_faces_webcam)

    def load_image(self):
        """Load an image from file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def detect_faces(self):
        """Detect faces, name, age & gender in the loaded image."""
        if self.image_path:
            img = cv2.imread(self.image_path)
            img = self.process_image(img)
            self.display_image(img)

    def start_webcam(self):
        """Start real-time face recognition using webcam."""
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def detect_faces_webcam(self):
        """Detect faces, name, age & gender in real-time webcam feed."""
        ret, frame = self.cap.read()
        if ret:
            frame = self.process_image(frame)
            self.display_image(frame)

    def stop_webcam(self):
        """Stop the webcam feed."""
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.label.clear()

    def process_image(self, img):
        """Detect faces, match names, and predict age & gender."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face_roi = img[y:y + h, x:x + w]

            # Predict Age & Gender
            age, gender = self.predict_age_gender(face_roi)

            # Recognize Known Faces
            name = self.recognize_face(face_roi)

            # Draw rectangle & label
            label = f"{name}, {gender}, {age}"
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return img

    def predict_age_gender(self, face_roi):
        """Predict age and gender from the detected face."""
        blob = cv2.dnn.blobFromImage(face_roi, 1, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
        
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        gender = GENDER_LABELS[gender_preds[0].argmax()]

        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = AGE_LABELS[age_preds[0].argmax()]

        return age, gender

    def recognize_face(self, face_roi):
        """Compare with known faces and return the name."""
        for filename, name in KNOWN_FACES.items():
            known_img = cv2.imread(f"faces/{filename}")
            known_gray = cv2.cvtColor(known_img, cv2.COLOR_BGR2GRAY)
            face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            if known_gray.shape == face_gray.shape:
                diff = cv2.absdiff(known_gray, face_gray).sum()
                if diff < 100000:  # Small difference means match
                    return name

        return "Unknown"

    def display_image(self, img):
        """Convert image to QImage and display in PyQt label."""
        h, w, ch = img.shape
        bytes_per_line = ch * w
        q_image = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        """Release webcam resources on close."""
        self.stop_webcam()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec_())

main()
