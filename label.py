import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Input Example")
        self.setGeometry(700, 300, 400, 300)

        self.label = QLabel("Enter your name:", self)
        self.label.move(50, 50)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(50, 80, 200, 30)

        button = QPushButton("Submit", self)
        button.setGeometry(50, 120, 100, 40)
        button.clicked.connect(self.update_label)

    def update_label(self):
        name = self.textbox.text()
        self.label.setText(f"Hello, {name}!")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

main()
