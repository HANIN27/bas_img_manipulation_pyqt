import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Viewer with Filters")
        self.setGeometry(400, 200, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 640, 480)

        self.button_gray = QPushButton("Grayscale", self)
        self.button_edge = QPushButton("Edge Detection", self)
        self.button_normal = QPushButton("Normal", self)

        self.button_gray.clicked.connect(lambda: self.set_filter("gray"))
        self.button_edge.clicked.connect(lambda: self.set_filter("edge"))
        self.button_normal.clicked.connect(lambda: self.set_filter("normal"))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_gray)
        layout.addWidget(self.button_edge)
        layout.addWidget(self.button_normal)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.current_filter = "normal"

    def set_filter(self, filter_type):
        self.current_filter = filter_type

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            if self.current_filter == "gray":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif self.current_filter == "edge":
                frame = cv2.Canny(frame, 50, 150)

            if len(frame.shape) == 2:
                h, w = frame.shape
                bytes_per_line = w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
            else:
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            self.label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec_())

main()
