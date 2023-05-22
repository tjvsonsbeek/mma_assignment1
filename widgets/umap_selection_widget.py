class Scatterplot(QWidget):
    selected_points_changed = pyqtSignal(list)
    selected_idx_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.points = np.random.rand(100, 2)      
        self.mean_x = np.mean(self.points[:, 0])
        self.mean_y = np.mean(self.points[:, 1])
        self.start_point = None
        self.end_point = None
        self.selected_points = []
        self.selected_idx = []
        self.setFixedSize(300, 300)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)
        qp.setBrush(QBrush(QColor(0, 0, 255, 100)))  # Set the fill color to transparent blue
        for x, y in self.points:
            qp.drawEllipse(QPoint(x * self.width(), y * self.height()), 5, 5)

        if self.start_point and self.end_point:
            rect = QRect(self.start_point, self.end_point)
            qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
            qp.drawRect(rect)

            self.selected_points = []
            self.selected_idx = []
            for i, (x, y) in enumerate(self.points):
                point = QPoint(x * self.width(), y * self.height())
                if rect.contains(point):
                    self.selected_points.append((self.points[:,0], self.points[:,1]))
                    self.selected_idx.append(i)

            self.selected_points_changed.emit(self.selected_points)
            self.selected_idx_changed.emit(self.selected_idx)
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
        if event.button() == Qt.RightButton:
            self.start_point = event.pos()
            self.update()

