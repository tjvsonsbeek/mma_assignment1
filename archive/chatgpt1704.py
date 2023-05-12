import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap

class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        # Create widgets
        self.image_label = QLabel()
        self.image_button = QPushButton('Select Image')
        self.image_button.clicked.connect(self.select_image)

        self.dataset_label = QLabel('Textual Dataset:')
        self.dataset_input = QLineEdit()
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_data)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_button)

        dataset_layout = QHBoxLayout()
        dataset_layout.addWidget(self.dataset_label)
        dataset_layout.addWidget(self.dataset_input)
        layout.addLayout(dataset_layout)

        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def select_image(self):
        # Open file dialog to select image
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            # Show selected image
            pixmap = QPixmap(filename)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height()))

    def submit_data(self):
        # Get input data and do something with it
        image = self.image_label.pixmap().toImage() if self.image_label.pixmap() else None
        dataset = self.dataset_input.text()
        # Do something with the input data
        print('Image:', image)
        print('Dataset:', dataset)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())