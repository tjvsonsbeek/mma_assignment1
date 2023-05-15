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

        # dataloading
        points = np.random.rand(100, 2)
        tags = generate_random_word_list(100, words)
        
        self.setWindowTitle("Scatterplot Dashboard")
        label = QLabel("Current Mouse Position: ")
        scatterplot = Scatterplot(points)
        selected_scatterplot = SelectedScatterplot(tags)
        button_widget = ButtonWidget(tags)
        
        mean_x_label = QLabel(f"Mean X: {scatterplot.mean_x:.2f}")
        mean_y_label = QLabel(f"Mean Y: {scatterplot.mean_y:.2f}")
        

        selected_points_label = QLabel()
        hbox = QHBoxLayout()
        hbox.addWidget(mean_x_label)
        hbox.addWidget(mean_y_label)
        hbox.addWidget(label)
        
        

        vbox = QVBoxLayout()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(scatterplot)
        hbox2.addWidget(button_widget)
        hbox2.addWidget(selected_scatterplot)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(selected_points_label)

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)
        print('check')
        scatterplot.selected_idx.connect(selected_scatterplot.set_selected_points)
        scatterplot.label.connect(label.setText)
        selected_scatterplot.top_words_changed.connect(button_widget.rename_buttons)
        button_widget.buttonClicked.connect(scatterplot.draw_scatterplot)
        button_widget.checkboxToggled.connect(scatterplot.set_outside_points_visible)

        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())