from PyQt6.QtCore import Qt, QSize,pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel
from PIL.ImageQt import ImageQt
from wordcloud import WordCloud

import sys


class ButtonWidget(QWidget):
    # Define custom signals
    buttonClicked = pyqtSignal(list)
    buttonUnclicked = pyqtSignal(list)
    checkboxToggled = pyqtSignal(bool)
    def __init__(self, tags, num_buttons=5):
        super().__init__()
        
        self.tags = tags
        self.num_buttons = num_buttons
        # Initialize selected word index
        self.selectedWordIndex = None

            
        # Create buttons for top words
        self.topWords = []

        self.buttons = []
        self.buttonLayout = QVBoxLayout()
        for i in range(self.num_buttons):
            button = QPushButton("")
            button.setCheckable(True)
            button.clicked.connect(lambda checked, i=i: self.onButtonClicked(i))
            button.toggled.connect(lambda checked, i=i: self.onButtonToggled(checked, i))
            self.buttons.append(button)
            self.buttonLayout.addWidget(button)


        # Create checkbox
        self.checkbox = QCheckBox("Also show points out of the rectangle area")
        self.checkbox.toggled.connect(self.onCheckboxToggled)
        self.buttonLayout.addWidget(self.checkbox)
        
        
        # Create layout for widget
        layout = QHBoxLayout()
        layout.addLayout(self.buttonLayout)
        layout.addStretch()
        self.setLayout(layout)
        
        
    def onButtonClicked(self, index):
        if index != self.selectedWordIndex:
            # Uncheck previously selected button, if any
            if self.selectedWordIndex is not None:
                self.buttons[self.selectedWordIndex].setChecked(False)

            # Update selected word index and emit signal with indices of points to highlight
            self.selectedWordIndex = index
            self.buttonClicked.emit(self.find_indices_with_tag(self.buttons[index].text().split(':')[0]))

    def onButtonToggled(self, checked, index):
        if not checked:
            # If the button was unchecked, emit the unclicked signal
            self.selectedWordIndex = None
            self.buttonUnclicked.emit([])
    def onCheckboxToggled(self, checked):
        self.checkboxToggled.emit(checked)

    def rename_buttons(self, topwords):
        self.topWords = topwords
        print(topwords)
        for i, word in enumerate(self.topWords[:self.num_buttons]):
            self.buttons[i].setText("{}: {}".format(word[0],word[1]))
        if len(topwords) < self.num_buttons:
            for i in range(len(topwords),self.num_buttons):
                self.buttons[i].setText("")
            
    def find_indices_with_tag(self,tag):
        indices = []
        for i, string in enumerate(self.tags):
            if tag in string and tag != "":
                indices.append(i)
        return indices