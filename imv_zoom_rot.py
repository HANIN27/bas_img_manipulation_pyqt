import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QTransform

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Image Viewer")
        self.setGeometry(500, 200, 600, 500)

        self.label = QLabel(self)
        self.label.setScaledContents(True)

        self.open_button = QPushButton("Open Image")
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_out_button = QPushButton("Zoom Out")
        self.rotate_button = QPushButton("Rotate")

        self.open_button.clicked.connect(self.open_image)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.rotate_button.clicked.connect(self.rotate_image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)
        layout.addWidget(self.rotate_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.pixmap = None
        self.scale_factor = 1.0
        self.rotation_angle = 0

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.pixmap = QPixmap(file_path)
            self.label.setPixmap(self.pixmap)

    def zoom_in(self):
        if self.pixmap:
            self.scale_factor *= 1.2
            self.update_image()

    def zoom_out(self):
        if self.pixmap:
            self.scale_factor *= 0.8
            self.update_image()

    def rotate_image(self):
        if self.pixmap:
            self.rotation_angle += 90
            self.update_image()

    def update_image(self):
        if self.pixmap:
            transformed = self.pixmap.transformed(QTransform().rotate(self.rotation_angle))
            scaled = transformed.scaled(self.pixmap.width() * self.scale_factor, self.pixmap.height() * self.scale_factor)
            self.label.setPixmap(scaled)

def main():
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())

main()
