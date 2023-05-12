import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from wordcloud import WordCloud, STOPWORDS


class WordCloudWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set window dimensions
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Word Cloud')

        # Generate word cloud image
        wc = WordCloud(background_color="white", width=800, height=600, stopwords=set(STOPWORDS))
        wc.generate_from_frequencies(self.generate_words())

        # Convert image to QPixmap and add to QLabel
        image = QImage(wc.to_array())
        pixmap = QPixmap.fromImage(image)
        label = QLabel(self)
        label.setPixmap(pixmap)

        # Set up QVBoxLayout and add QLabel to layout
        vbox = QVBoxLayout()
        vbox.addWidget(label)

        # Set layout and show window
        self.setLayout(vbox)
        self.show()

    def generate_words(self):
        # Generate frequency distribution of 100 random words
        words = {}
        for i in range(100):
            word = ''
            for j in range(random.randint(1, 10)):
                word += chr(random.randint(97, 122))
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
        return words


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordCloudWidget()
    sys.exit(app.exec_())