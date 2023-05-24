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
        
        self.wordcloud_background = config['wordcloud']['background_color']
        
        ## widget layout
        self.layout = QVBoxLayout(self)
        self.label = QLabel()
        self.layout.addWidget(self.label)

        
        ## initialize wordcloud with all points from scatterplot
        self.selected_points = None
        self.set_selected_points(list(range(len(tags))))

    def set_selected_points(self, selected_points):
        """set the selected points and updates the wordcloud"""
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
        """draw a wordcloud"""
        
        # compute the word frequencies
        word_counts = {}
        for tag in selected_tags:
            if tag in word_counts:
                word_counts[tag] += 1
            else:
                word_counts[tag] = 1
                
        self.wordcloud = WordCloud(background_color=self.wordcloud_background).generate_from_frequencies(word_counts)
        
        # saving wordcloud as png to to prevent the wordcloud from being distorted when resizing the window and converting it to a pixmap
        self.wordcloud.to_file("wordcloud.png")
        pixmap = QPixmap("wordcloud.png")
        
        # remove previous wordcloud
        self.label.clear()
        
        self.label.setPixmap(pixmap)
        
        # compute the top words and emit a signal with the word frequencies in sorted order
        top_words = self.get_top_words(word_counts)
        self.top_words_changed.emit(top_words)
    def get_top_words(self,word_counts):
        """Method that returns the word frequncies from the wordcloud sorted from most to least frequent"""
        sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_word_counts
    
