import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 500, 500)

        label = QLabel(self)
        label.setGeometry(0, 0, 500, 500)

        pixmap = QPixmap("C:/Users/Dr. HOMEIRA NISHAT/Desktop/pyqt sam/photu.png")  
        label.setPixmap(pixmap)

        label.setScaledContents(True)

        # Centering the image properly
        label.move((self.width() - label.width()) // 2, 
                   (self.height() - label.height()) // 2)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
