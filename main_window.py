import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt6.QtGui import QPainter, QMouseEvent, QPen,QBrush,QColor,QPixmap,QImage
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal  
from PIL.ImageQt import ImageQt

import random
import string
from wordcloud import WordCloud

from umap_selection_matplotlib import Scatterplot
from wordcloud_widget import SelectedScatterplot
from button_widget import ButtonWidget
import numpy as np

import random
words = ["apple", "banana", "orange", "grape", "kiwi"]

def generate_random_word_list(n, word_list):
    word_list_size = len(word_list)
    random_word_list = []

    for _ in range(n):
        random_word = random.choice(word_list)
        random_word_list.append(random_word)

    return random_word_list        
        
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ## dataloading
        points = np.random.rand(100, 2)
        tags = generate_random_word_list(100, words)
        
        ## inialize widgets
        scatterplot = Scatterplot(points)
        selected_scatterplot = SelectedScatterplot(tags)
        button_widget = ButtonWidget(tags)
        
        ## set up main window 
        self.setWindowTitle("Scatterplot Dashboard")
        label = QLabel("Current Mouse Position: ")
        selected_points_label = QLabel()
        mean_x_label = QLabel(f"Mean X: {scatterplot.mean_x:.2f}")
        mean_y_label = QLabel(f"Mean Y: {scatterplot.mean_y:.2f}")
        
        ## set up layout for header
        hbox = QHBoxLayout()
        hbox.addWidget(mean_x_label)
        hbox.addWidget(mean_y_label)
        hbox.addWidget(label)
        
        ## set up layout for widgets
        hbox2 = QHBoxLayout()
        hbox2.addWidget(scatterplot)
        hbox2.addWidget(button_widget)
        hbox2.addWidget(selected_scatterplot)
        
        ## set up layout for the full window
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(selected_points_label)

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)
        
        ## connect signals and slots 
        
        # connect selected indices from scatterplot to the wordcloud       
        scatterplot.selected_idx.connect(selected_scatterplot.set_selected_points)
        # set the label in the header to the current mouse position
        scatterplot.label.connect(label.setText)
        # connect the top words in the wordcloud to the buttons
        selected_scatterplot.top_words_changed.connect(button_widget.rename_buttons)
        # highlight the pointss with the associated tag of the button in the scatterplot
        button_widget.buttonClicked.connect(scatterplot.draw_scatterplot)
        # toggle the visibility of the points outside the selected rectangular region
        button_widget.checkboxToggled.connect(scatterplot.set_outside_points_visible)

        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())