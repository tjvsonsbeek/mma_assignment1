import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPen,QImage
from PyQt5.QtCore import Qt, QRectF
from wordcloud import WordCloud
from sklearn.manifold import TSNE
from PIL.ImageQt import ImageQt
import random
import string

def generate_word(length):
    """Generates a random word of the given length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_word_list(n, length):
    """Generates a list of n random words of the given length"""
    return [generate_word(length) for i in range(n)]

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.setLayout(vbox)
        vbox.addLayout(hbox)

        # Set up the t-SNE plot
        self.tsne_scene = QGraphicsScene()
        self.tsne_view = QGraphicsView(self.tsne_scene)
        hbox.addWidget(self.tsne_view)

        # Set up the wordcloud
        self.wordcloud_scene = QGraphicsScene()
        self.wordcloud_view = QGraphicsView(self.wordcloud_scene)
        hbox.addWidget(self.wordcloud_view)

        # Set up the buttons
        self.load_button = QPushButton('Load Data', self)
        self.load_button.clicked.connect(self.load_data)
        vbox.addWidget(self.load_button)

        self.select_button = QPushButton('Select Area', self)
        self.select_button.clicked.connect(self.select_area)
        vbox.addWidget(self.select_button)

    def load_data(self):
        # Load the data from file
        # file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'CSV Files (*.csv)')
        data = np.random.rand(100, 100)
        tags = generate_word_list(100, 5)

        # Compute the t-SNE embedding
        tsne = TSNE(n_components=2, random_state=0)
        tsne_data = tsne.fit_transform(data)

        # Plot the t-SNE embedding
        self.tsne_scene.clear()
        min_x = np.min(tsne_data[:, 0])
        max_x = np.max(tsne_data[:, 0])
        min_y = np.min(tsne_data[:, 1])
        max_y = np.max(tsne_data[:, 1])
        for i in range(len(tags)):
            x = tsne_data[i, 0]
            y = tsne_data[i, 1]
            tag = tags[i]
            brush = QBrush(QColor(*self.color(tag)))
            pen = QPen(QColor(*self.color(tag)))
            item = QGraphicsRectItem(QRectF(x, y, 2, 2))
            item.setBrush(brush)
            item.setPen(pen)
            self.tsne_scene.addItem(item)
        self.tsne_view.setSceneRect(min_x - 10, min_y - 10, max_x - min_x + 20, max_y - min_y + 20)

        # Compute the wordcloud
        self.wordcloud_scene.clear()
        word_counts = {}
        for i in range(len(tags)):
            if min_x <= tsne_data[i, 0] <= max_x and min_y <= tsne_data[i, 1] <= max_y:
                tag = tags[i]
                if tag in word_counts:
                    word_counts[tag] += 1
                else:
                    word_counts[tag] = 1
        wordcloud = WordCloud(width=800, height=600, background_color='white').generate_from_frequencies(word_counts)

        # Plot the wordcloud
        

        wordcloud_image = wordcloud.to_image()
        wordcloud_pixmap = wordcloud_pixmap = QPixmap.fromImage(ImageQt(wordcloud_image))
        wordcloud_item = QGraphicsPixmapItem(wordcloud_pixmap)
        self.wordcloud_scene.addItem(wordcloud_item)
        self.wordcloud_view.setSceneRect(0, 0, wordcloud_pixmap.width(), wordcloud_pixmap.height())

    def select_area(self):
        # Get the selection area from the user
        rect = self.tsne_view.sceneRect()
        selection_rect = self.tsne_view.mapToScene(self.tsne_view.rect()).boundingRect()
        selection_rect.setX(selection_rect.x() - rect.x())
        selection_rect.setY(selection_rect.y() - rect.y())

        # Update the wordcloud
        self.wordcloud_scene.clear()
        word_counts = {}
        for item in self.tsne_scene.items(selection_rect):
            tag = item.pen().color().name()
            if tag in word_counts:
                word_counts[tag] += 1
            else:
                word_counts[tag] = 1
        wordcloud = WordCloud(width=800, height=600, background_color='white').generate_from_frequencies(word_counts)

        # Plot the wordcloud
        wordcloud_image = wordcloud.to_image()
        wordcloud_pixmap = wordcloud_pixmap = QPixmap.fromImage(ImageQt(wordcloud_image))
        wordcloud_item = QGraphicsPixmapItem(wordcloud_pixmap)
        self.wordcloud_scene.addItem(wordcloud_item)
        self.wordcloud_view.setSceneRect(0, 0, wordcloud_pixmap.width(), wordcloud_pixmap.height())

    def color(self, tag):
        # Generate a color based on the tag
        if len(tag) != 6:
            # Return a default color if the tag is not a valid hex code
            return (128, 128, 128)
        try:
            r = int(tag[:2], 16)
            g = int(tag[2:4], 16)
            b = int(tag[4:], 16)
        except ValueError:
            # Return a default color if the tag is not a valid hex code
            return (128, 128, 128)
        return (r, g, b)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())