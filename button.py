import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Button Example")
        self.setGeometry(700, 300, 400, 300)

        button = QPushButton("Click Me", self)
        button.setGeometry(150, 130, 100, 40)
        button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        print("Button was clicked!")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

main()
