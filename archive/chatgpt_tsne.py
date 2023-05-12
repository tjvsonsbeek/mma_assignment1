import sys
import numpy as np
from sklearn.manifold import TSNE
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        # Create widgets
        self.vector_label = QLabel('Vector File:')
        self.vector_button = QPushButton('Select Vector File')
        self.vector_button.clicked.connect(self.select_vector)

        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot_tsne)

        # Set layout
        layout = QVBoxLayout()

        vector_layout = QHBoxLayout()
        vector_layout.addWidget(self.vector_label)
        vector_layout.addWidget(self.vector_button)
        layout.addLayout(vector_layout)

        layout.addWidget(self.plot_button)

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def select_vector(self):
        # Open file dialog to select vector file
        # filename, _ = QFileDialog.getOpenFileName(self, "Open Vector File", "", "Vector Files (*.npy)")
        # if filename:
        #     # Load vector file
        #     self.vectors = np.load(filename)
        self.vectors=np.random.rand(100,100)
    def plot_tsne(self):
        # Run t-SNE on the vectors
        tsne = TSNE(n_components=2, random_state=0)
        vectors_tsne = tsne.fit_transform(self.vectors)

        # Clear the previous plot
        self.figure.clear()

        # Plot the t-SNE points
        ax = self.figure.add_subplot(111)
        ax.scatter(vectors_tsne[:, 0], vectors_tsne[:, 1])

        # Draw the canvas
        self.canvas.draw()

class SelectedScatterplot(QWidget):
    def __init__(self):
        super().__init__()
        self.tags = generate_word_list(100, 5)
        self.selected_points = list(range(100))
        self.setFixedSize(300, 300)
    def set_selected_points(self, selected_points):
        self.selected_points = selected_points
        self.update()
        print('cjecl')


    def paintEvent(self, event):
        
        selected_tags = tags
        # Convert the list of tags to a string with space-separated words
        
        tag_str = " ".join(selected_tags)

        # Create a WordCloud object
        self.wordcloud = WordCloud(width=400, height=300, background_color="white").generate(tag_str)

        # Set up the widget layou
        layout = QVBoxLayout()
        layout.addWidget(self)
        self.setLayout(layout)
        
        # Draw the word cloud using a QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.drawImage(self.rect(), self.wordcloud.to_image())
        painter.end()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())