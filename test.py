
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal  
from PyQt6.QtGui import QPixmap
from PIL.ImageQt import ImageQt


from wordcloud import WordCloud



class WordcloudWidget(QWidget):
    top_words_changed = pyqtSignal(list)
    
    def __init__(self, tags):
        super().__init__()
        # Data setup and widget parameters
        self.tags = tags
        
        self.label = QLabel()
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)
        self.generate_wordcloud()

        

    def generate_wordcloud(self):
        # Prepare your text data
        text = " ".join(self.tags)

        # Create the word cloud object and generate the word cloud
        wordcloud = WordCloud(width=800, height=400).generate(text)
        self.label.setPixmap(QPixmap.fromImage(ImageQt(wordcloud.to_image())))
        self.show()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    tags = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "Nullam", "convallis",
            "eros", "ac", "tortor", "lobortis", "sit", "amet", "pharetra", "mi", "congue", "Vestibulum", "ante",
            "ipsum", "primis", "in", "faucibus", "orci", "luctus", "et", "ultrices", "posuere", "cubilia", "curae",
            "Sed", "suscipit", "malesuada", "nisl", "id", "suscipit", "Nam", "in", "nisl", "nec", "turpis", "cursus",
            "euismod", "Integer", "nec", "risus", "sapien", "Nullam", "pharetra", "diam", "ac", "nibh", "elementum",
            "a", "ultrices", "purus", "scelerisque", "Aliquam", "tincidunt", "metus", "vel", "pellentesque",
            "ullamcorper", "urna", "sapien", "luctus", "risus", "sit", "amet", "finibus", "justo", "tellus", "id",
            "massa"]

    window = WordcloudWidget(tags)
    window.show()

    sys.exit(app.exec())