import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget
import configparser
from widgets.embbedding_scatterplot_widget import ScatterplotWidget
from widgets.wordcloud_widget import WordcloudWidget
from widgets.button_widget import ButtonWidget
from widgets.image_widget import ImageWidget
import numpy as np
import pandas as pd
import h5py
import umap
from sklearn.manifold import TSNE



class MainWindow(QMainWindow):
    def compute_umap(self, image_features):
        return umap.UMAP(n_neighbors=6, n_components=2, metric='cosine').fit_transform(image_features)
    def compute_tsne(self, image_features):
        return TSNE(n_components=2, perplexity=30, n_iter=1000, metric='cosine').fit_transform(image_features)
    def make_layout(self, scatterplot, wordcloud, button_widget, image_widget,label):        
        self.setWindowTitle("Scatterplot Dashboard")
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
        hbox2.addWidget(wordcloud)
        
        ## set up layout for the full window
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(selected_points_label)
        vbox.addWidget(image_widget)

        ## set the layout of the main window
        main_widget = QWidget()
        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)
        
    def __init__(self):
        super().__init__()
        #load the config file 'config.ini'
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        data_path = config['main']['pkl_path']
        images_path = config['main']['images_path']
        
        num_samples = int(config['main']['num_samples'])
        sample_selection = str(config['main']['sample_selection'])
        ## dataloading
        df = pd.read_pickle(data_path)
        with h5py.File(images_path, "r") as hf:
            image_features = hf["image_features"][:]
            
        ## select num_samples samples between
        if sample_selection == 'random':
            random_indices = np.random.choice(len(df), num_samples, replace=False)
            tags = df['tags'].iloc[random_indices].values
            points = df[['umap_x','umap_y']].iloc[random_indices].values
            image_features = image_features[random_indices]
            img_paths = df['filepaths'].iloc[random_indices].values

        if sample_selection == 'first':
            tags = df['tags'].iloc[:num_samples].values
            points = df[['umap_x','umap_y']].iloc[:num_samples].values
            image_features = image_features[:num_samples]
            img_paths = df['filepaths'].iloc[:num_samples].values
        ## recompute the embedding coordinates
        if bool(config['main']['recompute_embedding']):
            if str(config['main']['embedding'])=='umap':
                points = self.compute_umap(image_features)
            elif str(config['main']['embedding'])=='tsne':
                points = self.compute_tsne(image_features)
                

        ## inialize widgets
        scatterplot = ScatterplotWidget(points, config)
        wordcloud = WordcloudWidget(tags, config)
        button_widget = ButtonWidget(tags, config)
        image_widget = ImageWidget(img_paths, config)
        label = QLabel("Current Mouse Position: ")

        
        ## set up main window 
        self.make_layout(scatterplot, wordcloud, button_widget, image_widget,label)
        
        ## connect signals and slots 
        
        # connect selected indices from scatterplot to the wordcloud       
        scatterplot.selected_idx.connect(wordcloud.set_selected_points)
        scatterplot.selected_idx.connect(button_widget.uncheck_all_buttons)
        scatterplot.selected_idx.connect(image_widget.set_selected_points)
        # set the label in the header to the current mouse position
        scatterplot.label.connect(label.setText)
        # connect the top words in the wordcloud to the buttons
        wordcloud.top_words_changed.connect(button_widget.rename_buttons)
        # highlight the points with the associated tag of the button in the scatterplot
        button_widget.buttonClicked.connect(scatterplot.draw_scatterplot)
        button_widget.buttonClicked.connect(image_widget.set_selected_points_button)
        # toggle the visibility of the points outside the selected rectangular region
        button_widget.checkboxToggled.connect(scatterplot.set_outside_points_visible)

        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())