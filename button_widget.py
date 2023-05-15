from PyQt6.QtCore import Qt, QSize,pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel
from PIL.ImageQt import ImageQt
from wordcloud import WordCloud

import sys


class ButtonWidget(QWidget):
    # Define signals
    buttonClicked = pyqtSignal(list)
    checkboxToggled = pyqtSignal(bool)
    def __init__(self, tags, num_buttons=5):
        super().__init__()
        ## data setup and widget parameters
        self.tags = tags
        self.num_buttons = num_buttons
        
        # Initialize selected button index
        self.selectedButtonIndex = None

            
        # Create buttons
        self.buttons = []
        self.buttonLayout = QVBoxLayout()
        for i in range(self.num_buttons):
            button = QPushButton("")
            button.setCheckable(True)
            button.clicked.connect(lambda checked, i=i: self.onButtonClicked(i))
            # button.toggled.connect(lambda checked, i=i: self.onButtonToggled(checked, i))
            self.buttons.append(button)
            self.buttonLayout.addWidget(button)

        # Create checkbox
        self.checkbox = QCheckBox("Show points out of the selected area")
        self.checkbox.toggled.connect(self.onCheckboxToggled)
        self.buttonLayout.addWidget(self.checkbox)
        

        # Create layout for widget
        layout = QHBoxLayout()
        layout.addLayout(self.buttonLayout)
        layout.addStretch()
        self.setLayout(layout)
        
        
    def onButtonClicked(self, index):
        """if the button is unchecked, check and emit the clicked signal, else uncheck and emit the unclicked signal. The emitted signal contains the indices of the points that have the tag of the button."""
        if self.buttons[index].isChecked():
            if self.selectedButtonIndex is not None:
                self.buttons[self.selectedButtonIndex].setChecked(False)
            self.selectedButtonIndex = index
            self.buttons[index].setChecked(True)
            self.buttonClicked.emit(self.find_indices_with_tag(self.buttons[index].text().split(':')[0]))
        else:
            self.buttons[index].setChecked(False)
            self.buttonClicked.emit([])
            
    def onCheckboxToggled(self, checked):
        """Emit signal with checkbox state"""
        self.checkboxToggled.emit(checked)

    def rename_buttons(self, topwords):
        """Rename buttons with top words. The button will be empty if there are less than self.num_buttons words."""
        self.topWords = topwords
        print(topwords)
        for i, word in enumerate(self.topWords[:self.num_buttons]):
            self.buttons[i].setText("{}: {}".format(word[0],word[1]))
        if len(topwords) < self.num_buttons:
            for i in range(len(topwords),self.num_buttons):
                self.buttons[i].setText("")
            
    def find_indices_with_tag(self,tag):
        """Find indices of points with a given tag. These are used to connect words in the wordcloud with points in the scatterplot."""
        indices = []
        for i, string in enumerate(self.tags):
            if tag in string and tag != "":
                indices.append(i)
        return indices