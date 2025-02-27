import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

class FaceDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Detection - Image & Webcam")
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
        """Detect faces in the loaded image."""
        if self.image_path:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            img = cv2.imread(self.image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            h, w, ch = img.shape
            bytes_per_line = ch * w
            q_image = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(q_image))

    def start_webcam(self):
        """Start real-time face detection using webcam."""
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def detect_faces_webcam(self):
        """Detect faces from live webcam feed."""
        ret, frame = self.cap.read()
        if ret:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(q_image))

    def stop_webcam(self):
        """Stop the webcam feed."""
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.label.clear()

    def closeEvent(self, event):
        """Release webcam resources on close."""
        self.stop_webcam()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = FaceDetectionApp()
    window.show()
    sys.exit(app.exec_())

main()
