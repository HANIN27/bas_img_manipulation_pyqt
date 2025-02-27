import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Form")
        self.setGeometry(600, 300, 300, 200)

        self.label_user = QLabel("Username:", self)
        self.label_user.move(20, 30)
        self.text_user = QLineEdit(self)
        self.text_user.setGeometry(100, 30, 150, 25)

        self.label_pass = QLabel("Password:", self)
        self.label_pass.move(20, 70)
        self.text_pass = QLineEdit(self)
        self.text_pass.setGeometry(100, 70, 150, 25)
        self.text_pass.setEchoMode(QLineEdit.Password)

        self.button = QPushButton("Login", self)
        self.button.setGeometry(100, 110, 100, 30)
        self.button.clicked.connect(self.validate_login)

    def validate_login(self):
        username = self.text_user.text()
        password = self.text_pass.text()
        if username == "admin" and password == "1234":
            QMessageBox.information(self, "Login Successful", "Welcome!")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials!")

def main():
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())

main()
