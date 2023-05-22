import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from widgets.umap_selection_matplotlib import ScatterplotWidget
from widgets.wordcloud_widget import WordcloudWidget
from widgets.button_widget import ButtonWidget
import numpy as np
import pandas as pd
import h5py

        
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ## dataloading
        df = pd.read_pickle('birds.pkl')
        points = np.zeros((1000,2))
        points[:,0] = df['umap_x'].values
        points[:,1] = df['umap_y'].values
        tags = df['tags'].values

        output_file = "image_features.h5"
        # add the UMAP coordinates to the dataframe
        with h5py.File(output_file, "r") as hf:
            image_features = hf["image_features"][:]

        
        ## inialize widgets
        scatterplot = ScatterplotWidget(image_features)
        wordcloud = WordcloudWidget(tags)
        button_widget = ButtonWidget(tags)
        
        ## set up main window 
        self.setWindowTitle("Scatterplot Dashboard")
        label = QLabel("Current Mouse Position: ")
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

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)
        
        ## connect signals and slots 
        
        # connect selected indices from scatterplot to the wordcloud       
        scatterplot.selected_idx.connect(wordcloud.set_selected_points)
        scatterplot.selected_idx.connect(button_widget.uncheck_all_buttons)
        # set the label in the header to the current mouse position
        scatterplot.label.connect(label.setText)
        # connect the top words in the wordcloud to the buttons
        wordcloud.top_words_changed.connect(button_widget.rename_buttons)
        # highlight the pointss with the associated tag of the button in the scatterplot
        button_widget.buttonClicked.connect(scatterplot.draw_scatterplot)
        # toggle the visibility of the points outside the selected rectangular region
        button_widget.checkboxToggled.connect(scatterplot.set_outside_points_visible)

        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())