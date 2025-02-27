import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Capture")
        self.setGeometry(300, 200, 640, 480)

        # Layout
        self.layout = QVBoxLayout()
        
        # QLabel to show camera feed
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        
        # Button to capture image
        self.capture_button = QPushButton("Capture Image")
        self.capture_button.clicked.connect(self.capture_image)
        self.layout.addWidget(self.capture_button)

        self.setLayout(self.layout)

        # OpenCV Camera
        self.cap = cv2.VideoCapture(0)  # 0 for default camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(q_img))

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
            print("Image Saved: captured_image.jpg")

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Sample App")
        self.initUI()

    def initUI(self):
        self.label = QLabel("First Label", self)
        self.label.move(50, 50)

        self.b1 = QPushButton("Open Camera", self)
        self.b1.move(50, 100)
        self.b1.clicked.connect(self.open_camera)

    def open_camera(self):
        self.camera_window = CameraWindow()
        self.camera_window.show()

def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
