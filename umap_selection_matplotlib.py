import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt6.QtGui import QPainter, QMouseEvent, QPen,QBrush,QColor,QPixmap,QImage
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal  
from PIL.ImageQt import ImageQt
import numpy as np
import random
import string
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.figure import Figure
import umap
import pandas as pd

class Scatterplot(QWidget):
    """Widget that displays a scatterplot and allows the user to select coordinates with mouse clicks that are displayed as a rectangle on the plot. The points encased by the rectangle are emitted as a signal."""
    
    
    # signal that emits the index of the selected points
    selected_idx = pyqtSignal(list)
    #signal that emits the current mouse position
    label = pyqtSignal(str)
    
    def __init__(self,points):
        super().__init__()
        self.setMouseTracking(True)
        
        # umap_embeddings = umap.UMAP(n_neighbors=5, n_components=2, metric='cosine').fit_transform(df['clip_embeddings'].tolist())
        # df['umap_x'] = umap_embeddings[:,0]
        # df['umap_y'] = umap_embeddings[:,1]
        self.points = points

        self.mean_x = np.mean(self.points[:,0])
        self.mean_y = np.mean(self.points[:,1])
        self.start_point = None
        self.end_point = None
        self.setFixedSize(300, 300)
        
        # create a matplotlib figure and add a subplot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        # set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        
        self.selected_points = []
        self.outside_points_visible = False
        self.draw_scatterplot()
        self.canvas.draw()
        
        
        
        #connect the mouse press event to the selection method
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        #connect the mouse move event to the label method
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
    
    def on_mouse_move(self, event):
        """Method that handles mouse movement on the canvas"""
        # Ignore mouse movement outside the plot area
        if event.inaxes is None:
            return
        x, y = event.xdata, event.ydata
        # emit a signal with the current mouse position
        self.label.emit(f"Current Mouse Position: {x:.2f}, {y:.2f}")
    
    def on_canvas_click(self, event):
        """Method that handles mouse clicks on the canvas"""
        # Ignore clicks outside the plot area
        if event.inaxes is None:
            print("click outside axes")
            return
        # left click to select points
        if event.button == 1:
            if not self.start_point:
                self.start_point = (event.xdata, event.ydata)
            else:
                self.end_point = (event.xdata, event.ydata)
                self.draw_selection_rectangle()
        
        # right click to select points
        elif event.button == 3:
            self.start_point = (event.xdata, event.ydata)
            if self.start_point and self.end_point:
                self.draw_selection_rectangle()

        
    def draw_selection_rectangle(self):
        """Method that draws the selection rectangle on the plot"""
        # get coordinates of the selection rectangle
        x1, y1 = self.start_point[0], self.start_point[1]
        x2, y2 = self.end_point[0], self.end_point[1]
        
        #calculate the position and size of the rectangle
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x1 - x2)
        h = abs(y1 - y2)
        
        #remove the old rectangle if it exists
        self.clear_selection()           
        # add the new rectangle to the plot
        self.rect = Rectangle((x, y), w, h, facecolor='red', alpha=0.5)
        self.ax.add_patch(self.rect)
        
        #update the plot
        self.canvas.draw()
        
        # emit a signal with the index of the selected points
        xmin, xmax = sorted([x1, x2])
        ymin, ymax = sorted([y1, y2])
        
        # get the indices of the selected points
        indices = [i for i, p in enumerate(self.points) if xmin <= p[0] <= xmax and ymin <= p[1] <= ymax]
        
        # update the selected points
        self.draw_scatterplot()
        
        # emit the signal
        self.selected_idx.emit(indices)
    def draw_scatterplot(self, selected_points=None):
        """method that makes a scatterplot in blue for all points. If points are selected these are plotted in red. leave the rectangle on the plot"""
        # remove the old points from the plot
        if selected_points!=None:
            self.selected_points = selected_points
        for point in self.ax.collections:
            point.remove()
        self.ax.scatter(self.points[:,0], self.points[:,1], s=5, c='blue')
    
        for i in self.selected_points:
            point = self.points[i]
            if self.is_point_in_rectangle(point) or self.outside_points_visible:
                self.ax.scatter(point[0], point[1], s=5, c='red')
        self.canvas.draw()
        
    def is_point_in_rectangle(self,point):
        """Method that checks if a point is in the selection rectangle"""
        # get the coordinates of the rectangle
        if self.start_point[0] < self.end_point[0]:
            x1, x2 = self.start_point[0], self.end_point[0]
        else:
            x1, x2 = self.end_point[0], self.start_point[0]
        if self.start_point[1] < self.end_point[1]:
            y1, y2 = self.start_point[1], self.end_point[1]
        else:   
            y1, y2 = self.end_point[1], self.start_point[1]
        
        # get the coordinates of the point
        x, y = point[0], point[1]

        # check if the point is in the rectangle
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        else:
            return False
        
    def set_outside_points_visible(self, visible):
        self.outside_points_visible = visible
        self.draw_scatterplot()
    def clear_selection(self):
        # Remove the rectangle from the plot
        for patch in self.ax.patches:
            patch.remove()
        
