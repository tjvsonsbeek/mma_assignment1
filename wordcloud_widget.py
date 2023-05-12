import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt6.QtGui import QPainter, QMouseEvent, QPen,QBrush,QColor,QPixmap,QImage
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal  
from PIL.ImageQt import ImageQt

import random
import string
from wordcloud import WordCloud

class SelectedScatterplot(QWidget):
    top_words_changed = pyqtSignal(list)
    def __init__(self,tags):
        super().__init__()
        self.tags = tags
        self.selected_points = list(range(100))
        self.setFixedSize(300, 300)
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        self.wordcloud_scene = QGraphicsScene()
        self.wordcloud_view = QGraphicsView(self.wordcloud_scene)
        hbox.addWidget(self.wordcloud_view)
        self.set_selected_points(self.selected_points, initial=True)
    def set_selected_points(self, selected_points, initial=False):
        if self.selected_points!=selected_points or initial:
            self.selected_points = selected_points
            selected_tags = []
            for i in self.selected_points:
                selected_tags.append("".join(self.tags[i]))
            selected_tags = ['empty'] if len(selected_tags) == 0 else selected_tags
            print(selected_tags)
            self.draw_wordcloud(selected_tags)
    
    def draw_wordcloud(self, selected_tags):
        self.wordcloud_scene.clear()
        word_counts = {}
        print(selected_tags)
        for tag in selected_tags:
            if tag in word_counts:
                word_counts[tag] += 1
            else:
                word_counts[tag] = 1
        print(word_counts)
        self.wordcloud = WordCloud(width=300, height=300, background_color='white').generate_from_frequencies(word_counts)

        # Plot the wordcloud
        wordcloud_image = self.wordcloud.to_image()
        wordcloud_pixmap = wordcloud_pixmap = QPixmap.fromImage(ImageQt(wordcloud_image))
        wordcloud_item = QGraphicsPixmapItem(wordcloud_pixmap)
        self.wordcloud_scene.addItem(wordcloud_item)
        self.wordcloud_view.setSceneRect(0, 0, wordcloud_pixmap.width(), wordcloud_pixmap.height())
        top_words = self.get_top_words(word_counts,5)
        self.top_words_changed.emit(top_words)
    def get_top_words(self,word_counts,n):
        sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        print(sorted_word_counts)
        return sorted_word_counts
       