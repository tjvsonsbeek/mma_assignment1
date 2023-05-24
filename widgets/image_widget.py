
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtWidgets import QGridLayout, QLabel
from PyQt6.QtGui import QPixmap
import os
import numpy as np
import random
class ImageWidget(QWidget):
    """pyqt widget that has as input a list of image path. It takes an input signal of indices. Based on that a random number of images is displayed (max n) in two rows"""
    def __init__(self,img_paths, config):
        super().__init__()
        self.base_path = "/home/tjvsonsbeek/Documents/Datasets/birds/"
        self.img_paths = img_paths
        self.images_per_row = 10
        self.rows = 2
        self.setGeometry(100,100,1000,200)
        
        
        self.imgs = []
        
        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(10)
        self.layout.setVerticalSpacing(10)
        
        self.selected_points = []
        self.selected_points_button = []
        self.set_selected_points([])
    def update(self):
        """Update the widget with the new indices"""
        # Remove all images from the layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.imgs = []
        # Add new images
        for i, img_path in enumerate(self.selected_images):
            col = i % self.images_per_row
            row = i // self.images_per_row
            self.create_image_labels(img_path, col, row)
    def create_image_labels(self,image_path, col, row):
        # for image_path in self.selected_images:
        pixmap = QPixmap(os.path.join(self.base_path,image_path))
        pixmap = pixmap.scaled(100, 100)  # Adjust the size of the images as needed
        label = QLabel(self)
        label.setPixmap(pixmap)
        self.layout.addWidget(label, row, col)
    def set_selected_points(self, selected_points):
        """Method that sets the selected points and updates the wordcloud"""
        ## only update the wordcloud if the selected points in the scatterplot have changed
        if selected_points==[]:
            self.selected_images = random.sample(self.img_paths.tolist(),min(len(self.img_paths),self.images_per_row*self.rows))
            self.update()
        if self.selected_points!=selected_points:
            self.selected_points = selected_points
            self.selected_images = random.sample(self.img_paths[self.selected_points].tolist(),min(len(self.img_paths[self.selected_points]),self.images_per_row*self.rows))
            self.update()
    def set_selected_points_button(self, selected_points):
        """Method that sets the selected points and updates the wordcloud"""
        if selected_points==[]:
            self.selected_images = random.sample(self.img_paths[self.selected_points].tolist(),min(len(self.img_paths[self.selected_points]),self.images_per_row*self.rows))
            self.update()
        else:
            self.selected_points_button = selected_points
            self.selected_images = random.sample(self.img_paths[np.intersect1d(self.selected_points_button,self.selected_points)].tolist(),min(len(self.img_paths[np.intersect1d(self.selected_points_button,self.selected_points)]),self.images_per_row*self.rows))
            self.update()
            



