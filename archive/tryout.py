from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World")
        button=QPushButton("Hello World")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)
        self.setCentralWidget(button)
    def the_button_was_clicked(self):
        my_popup=QMainWindow()
        my_popup.setWindowTitle("Popup!")
        print('clicked a button!')
        my_popup.show()
    def the_button_was_toggled(self, checked):
        print("Checked?",checked)
app = QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()