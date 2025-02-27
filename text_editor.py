import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QFileDialog, QVBoxLayout, QWidget

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Notepad")
        self.setGeometry(500, 200, 600, 400)

        self.text_edit = QTextEdit(self)

        save_button = QPushButton("Save File", self)
        save_button.clicked.connect(self.save_file)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())

def main():
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec_())

main()
