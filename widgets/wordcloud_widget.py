import sys

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal  
from PyQt6.QtGui import QPixmap
from PIL.ImageQt import ImageQt
from PIL import Image
import random
import string


from wordcloud import WordCloud


class WordcloudWidget(QWidget):
    top_words_changed = pyqtSignal(list)
    def __init__(self,tags, config):
        super().__init__()
        ## data setup and widget parameters
        self.tags = tags
        self.tag_separator = config['wordcloud']['tag_separator']
        
        ## widget layout
        self.layout = QVBoxLayout(self)
        self.label = QLabel()
        self.layout.addWidget(self.label)

        
        ## initialize wordcloud with all points from scatterplot
        self.selected_points = None
        self.set_selected_points(list(range(len(tags))))

    def set_selected_points(self, selected_points):
        """Method that sets the selected points and updates the wordcloud"""
        ## only update the wordcloud if the selected points in the scatterplot have changed
        if self.selected_points!=selected_points:
            self.selected_points = selected_points
            ## add all tags from the selected points to a list. tags are separated by a space
            selected_tags = []
            for i in self.selected_points:
                for t in self.tags[i].split(self.tag_separator):
                    selected_tags.append(t)
            selected_tags = [''] if len(selected_tags) == 0 else selected_tags
            self.draw_wordcloud(selected_tags)
    
    def draw_wordcloud(self, selected_tags):
        """Method that draws the wordcloud"""
        word_counts = {}
        print(selected_tags)
        for tag in selected_tags:
            if tag in word_counts:
                word_counts[tag] += 1
            else:
                word_counts[tag] = 1
        print(word_counts)
        self.wordcloud = WordCloud(width = 300, height = 300,background_color='white').generate_from_frequencies(word_counts)
        print(self.wordcloud)
        
        self.wordcloud.to_file("wordcloud.png")
        
        pixmap = QPixmap("wordcloud.png")
        self.label.clear()

        self.label.setPixmap(pixmap)
        
        
        
        top_words = self.get_top_words(word_counts,5)
        self.top_words_changed.emit(top_words)
    def get_top_words(self,word_counts,n):
        """Method that returns the top n words from the wordcloud"""
        sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        print(sorted_word_counts)
        return sorted_word_counts
       