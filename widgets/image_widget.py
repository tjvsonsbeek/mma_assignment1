
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtWidgets import QGridLayout, QLabel
from PyQt6.QtGui import QPixmap

class ImageWidget(QWidget):
    """pyqt widget that has as input a list of image path. It takes an input signal of indices. Based on that a random number of images is displayed (max n) in two rows"""
    def __init__(self,img_paths):
        super().__init__()
        self.img_paths = img_paths
        self.max_n = 10
        self.n = 0
        self.img_labels = []
        self.initUI()
    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
    def update(self):
        """Update the widget with the new indices"""
        # Remove all images
        for label in self.img_labels:
            self.layout.removeWidget(label)
            label.deleteLater()
        self.img_labels = []
        # Add new images
        for i in range(len(self.img_paths)):
            if i in self.selected_points:
                self.add_image(self.img_paths[i])
    def add_image(self,img_path):
        """Add an image to the widget"""
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaledToWidth(200)
        label = QLabel()
        label.setPixmap(pixmap)
        self.layout.addWidget(label,self.n//self.max_n,self.n%self.max_n)
        self.n += 1
        self.img_labels.append(label)
    def set_selected_points(self, selected_points):
        """Method that sets the selected points and updates the wordcloud"""
        ## only update the wordcloud if the selected points in the scatterplot have changed
        if self.selected_points!=selected_points:
            self.selected_points = selected_points
            self.update()

