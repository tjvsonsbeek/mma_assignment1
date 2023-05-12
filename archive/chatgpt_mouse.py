import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QMouseEvent, QPen
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal

import random

class Scatterplot(QWidget):
    selected_points_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.points = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(100)]
        self.mean_x = sum(x for x, _ in self.points) / len(self.points)
        self.mean_y = sum(y for _, y in self.points) / len(self.points)
        self.start_point = None
        self.end_point = None
        self.selected_points = []

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)
        qp.setBrush(Qt.red)
        for x, y in self.points:
            qp.drawEllipse(QPoint(x * self.width(), y * self.height()), 5, 5)

        if self.start_point and self.end_point:
            rect = QRect(self.start_point, self.end_point)
            qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
            qp.drawRect(rect)

            self.selected_points = []
            for x, y in self.points:
                point = QPoint(x * self.width(), y * self.height())
                if rect.contains(point):
                    self.selected_points.append((x, y))

            self.selected_points_changed.emit(self.selected_points)

        qp.end()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        x = event.x() / self.width()
        y = event.y() / self.height()
        label.setText(f"Current Mouse Position: ({x:.2f}, {y:.2f})")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if not self.start_point:
                self.start_point = event.pos()
            else:
                self.end_point = event.pos()
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scatterplot Dashboard")

        scatterplot = Scatterplot()
        mean_x_label = QLabel(f"Mean X: {scatterplot.mean_x:.2f}")
        mean_y_label = QLabel(f"Mean Y: {scatterplot.mean_y:.2f}")
        global label
        label = QLabel("Current Mouse Position: ")
        selected_points_label = QLabel()
        hbox = QHBoxLayout()
        hbox.addWidget(mean_x_label)
        hbox.addWidget(mean_y_label)
        hbox.addWidget(label)

        vbox = QVBoxLayout()
        vbox.addWidget(scatterplot)
        vbox.addLayout(hbox)
        vbox.addWidget(selected_points_label)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        scatterplot.selected_points_changed.connect(
            lambda points: selected_points_label.setText(f"Selected Points: {points}")
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
