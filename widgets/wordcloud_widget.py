import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt6.QtGui import QPainter, QMouseEvent, QPen,QBrush,QColor,QPixmap,QImage
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal  
from PIL.ImageQt import ImageQt

import random
import string
from wordcloud import WordCloud


class WordcloudWidget(QWidget):
    top_words_changed = pyqtSignal(list)
    def __init__(self,tags):
        super().__init__()
        ## data setup and widget parameters
        self.tags = tags
        # self.setFixedSize(300, 300)
        
        ## widget layout
        hbox = QVBoxLayout()
        self.setLayout(hbox)
        self.wordcloud_scene = QGraphicsScene()
        self.wordcloud_view = QGraphicsView(self.wordcloud_scene)
        hbox.addWidget(self.wordcloud_view)
        
        ## initialize wordcloud with all points from scatterplot
        self.selected_points = None
        self.set_selected_points(list(range(len(tags))))
        # Set initial widget size
        self.resize_widget()

    def resizeEvent(self, event):
        # Resize widget while keeping it square
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)
        self.resize_widget()

    def resize_widget(self):
        # Adjust Word Cloud size to fit the widget
        size = min(self.wordcloud_view.width(), self.wordcloud_view.height())
        self.wordcloud_view.setFixedSize(size, size)
    def set_selected_points(self, selected_points):
        """Method that sets the selected points and updates the wordcloud"""
        ## only update the wordcloud if the selected points in the scatterplot have changed
        if self.selected_points!=selected_points:
            self.selected_points = selected_points
            ## add all tags from the selected points to a list. tags are separated by a space
            selected_tags = []
            for i in self.selected_points:
                for t in self.tags[i].split(" "):
                    selected_tags.append(t)
            selected_tags = [''] if len(selected_tags) == 0 else selected_tags
            self.draw_wordcloud(selected_tags)
    
    def draw_wordcloud(self, selected_tags):
        """Method that draws the wordcloud"""
        self.wordcloud_scene.clear()
        word_counts = {}
        print(selected_tags)
        for tag in selected_tags:
            if tag in word_counts:
                word_counts[tag] += 1
            else:
                word_counts[tag] = 1
        print(word_counts)
        self.wordcloud = WordCloud(background_color='white').generate_from_frequencies(word_counts)

        # Plot the wordcloud
        wordcloud_image = self.wordcloud.to_image()
        wordcloud_pixmap = wordcloud_pixmap = QPixmap.fromImage(ImageQt(wordcloud_image))
        wordcloud_item = QGraphicsPixmapItem(wordcloud_pixmap)
        self.wordcloud_scene.addItem(wordcloud_item)
        self.wordcloud_view.setSceneRect(0, 0, wordcloud_pixmap.width(), wordcloud_pixmap.height())
        top_words = self.get_top_words(word_counts,5)
        self.top_words_changed.emit(top_words)
    def get_top_words(self,word_counts,n):
        """Method that returns the top n words from the wordcloud"""
        sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        print(sorted_word_counts)
        return sorted_word_counts
       