import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Image Viewer")
        self.setGeometry(500, 200, 600, 400)

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 500, 250)

        button = QPushButton("Open Image", self)
        button.setGeometry(250, 320, 100, 40)
        button.clicked.connect(self.open_image)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

main()
