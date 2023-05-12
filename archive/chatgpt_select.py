from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
import numpy as np
import sys
import matplotlib.pyplot as plt
import random

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Set the title and size of the window
        self.setWindowTitle("PyQt Dashboard")
        self.resize(600, 400)

        # Create a Figure and an Axes for the scatter plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        # Generate random points and plot them in the scatter plot
        self.x_values = [random.uniform(0, 10) for i in range(100)]
        self.y_values = [random.uniform(0, 10) for i in range(100)]
        self.ax.scatter(self.x_values, self.y_values)

        # Calculate and display the mean x and y values of all points
        self.mean_x = sum(self.x_values) / len(self.x_values)
        self.mean_y = sum(self.y_values) / len(self.y_values)
        self.mean_x_label = QLabel(f"Mean X Value: {self.mean_x:.2f}", self)
        self.mean_x_label.setGeometry(QRect(10, 320, 150, 20))
        self.mean_y_label = QLabel(f"Mean Y Value: {self.mean_y:.2f}", self)
        self.mean_y_label.setGeometry(QRect(10, 350, 150, 20))

        # Create a rectangle selector for the scatter plot
        self.selector = RectangleSelector(self.ax, self.update_mean_values, drawtype='box', useblit=True, button=[1],
                                           minspanx=5, minspany=5, spancoords='pixels')

        # Embed the Matplotlib plot into the PyQt widget
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.setGeometry(QRect(10, 10, 400, 300))
        self.canvas.draw()

    def update_mean_values(self, eclick, erelease):
        # Get the x and y coordinates of the selected rectangle
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        # Calculate and display the mean x and y values of the points within the selected rectangle
        selected_x = [x for x, y in zip(self.x_values, self.y_values) if x1 <= x <= x2 and y1 <= y <= y2]
        selected_y = [y for x, y in zip(self.x_values, self.y_values) if x1 <= x <= x2 and y1 <= y <= y2]
        if selected_x and selected_y:
            mean_x = sum(selected_x) / len(selected_x)
            mean_y = sum(selected_y) / len(selected_y)
            self.mean_x_label.setText(f"Mean X Value: {mean_x:.2f}")
            self.mean_y_label.setText(f"Mean Y Value: {mean_y:.2f}")
        else:
            self.mean_x_label.setText(f"Mean X Value: {self.mean_x:.2f}")
            self.mean_y_label.setText(f"Mean Y Value: {self.mean_y:.2f}")
import matplotlib.patches as patches

class RectangleSelector:
    def __init__(self, ax, onselect, drawtype='box', minspanx=None, minspany=None,
                 useblit=False, button=None, spancoords='data', rectprops=None,
                 onmove_callback=None):
        self.ax = ax
        self.onselect = onselect
        self.drawtype = drawtype
        self.minspanx = minspanx
        self.minspany = minspany
        self.useblit = useblit
        self.button = button
        self.spancoords = spancoords
        self.onmove_callback = onmove_callback

        if rectprops is None:
            rectprops = {'facecolor': 'blue', 'edgecolor': 'black', 'alpha': 0.5}

        self.rectprops = rectprops

        self.rect = None
        self.press = None
        self.background = None

        self.connect_events()

    def connect_events(self):
        self.cidpress = self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def disconnect_events(self):
        self.ax.figure.canvas.mpl_disconnect(self.cidpress)
        self.ax.figure.canvas.mpl_disconnect(self.cidrelease)
        self.ax.figure.canvas.mpl_disconnect(self.cidmotion)

    def on_press(self, event):
        if self.button is not None and event.button != self.button:
            return
        if event.inaxes != self.ax:
            return

        self.press = event.xdata, event.ydata

        if self.rect is not None:
            self.rect.remove()
            self.rect = None

        if self.drawtype == 'box':
            self.rect = patches.Rectangle(self.press, 0, 0, **self.rectprops)
        elif self.drawtype == 'line':
            self.rect = patches.FancyArrowPatch(self.press, self.press, **self.rectprops)
        else:
            raise ValueError('Unknown drawtype: %s' % self.drawtype)

        self.ax.add_patch(self.rect)

        if self.useblit:
            self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)

        self.ax.figure.canvas.draw()

    def on_release(self, event):
        if self.button is not None and event.button != self.button:
            return
        if event.inaxes != self.ax:
            return
        if self.press is None:
            return

        x0, y0 = self.press
        x1, y1 = event.xdata, event.ydata

        if self.minspanx is not None and abs(x1 - x0) < self.minspanx:
            self.rect.remove()
            self.rect = None
            self.ax.figure.canvas.draw()
            return

        if self.minspany is not None and abs(y1 - y0) < self.minspany:
            self.rect.remove()
            self.rect = None
            self.ax.figure.canvas.draw()
            return

        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0

        self.rect.set_bounds(x0, y0, x1 - x0, y1 - y0)

        if self.useblit:
            self.ax.figure.canvas.restore_region(self.background)
            self.ax.draw_artist(self.rect)
            self.ax.figure.canvas.blit(self.ax.bbox)

        self.press = None

        if self.onselect is not None:
            self.onselect(x0, y0, x1, y1)

    def on_motion(self, event):
        if self.button is not None and event.button != self.button:
            return
        if self.press is None:
            return
        if event.inaxes != self.ax:
            return

        x0, y0 = self.press
        x1, y1 = event.xdata, event.ydata

        if self.drawtype == 'box':
            self.rect.set_bounds(x0, y0, x1 - x0, y1 - y0)
        elif self.drawtype == 'line':
            self.rect.set_positions((x0, y0), (x1, y1))
        else:
            raise ValueError('Unknown drawtype: %s' % self.drawtype)

        if self.useblit:
            self.ax.figure.canvas.restore_region(self.background)
            self.ax.draw_artist(self.rect)
            self.ax.figure.canvas.blit(self.ax.bbox)
        else:
            self.ax.figure.canvas.draw()

        if self.onmove_callback is not None:
            self.onmove_callback(x0, y0, x1, y1)

    def disconnect(self):
        self.disconnect_events()
        if self.rect is not None:
            self.rect.remove()
        self.ax.figure.canvas.draw_idle()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
