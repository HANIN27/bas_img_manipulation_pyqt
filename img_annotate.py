import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QPoint

class ImageAnnotator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Annotation Tool")
        self.setGeometry(400, 200, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 640, 480)
        self.label.setPixmap(QPixmap(640, 480))
        self.label.pixmap().fill(Qt.white)

        self.button_load = QPushButton("Load Image", self)
        self.button_save = QPushButton("Save Image", self)

        self.button_load.clicked.connect(self.load_image)
        self.button_save.clicked.connect(self.save_image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_load)
        layout.addWidget(self.button_save)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.drawing = False
        self.last_point = QPoint()

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.label.setPixmap(QPixmap(file_path))

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.label.pixmap().save(file_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.label.pixmap())
            pen = QPen(Qt.red, 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.label.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

def main():
    app = QApplication(sys.argv)
    window = ImageAnnotator()
    window.show()
    sys.exit(app.exec_())

main()
