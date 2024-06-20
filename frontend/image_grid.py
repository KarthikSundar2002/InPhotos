from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize

import os

class ImageGrid(QWidget):
    def __init__(self, path="/home/stark/test"):
        super().__init__()
        self.layout = QGridLayout()
        self.columns = 4
        self.current_images = 0
        self.dir_path = path
        paths = [path + "/" + path for path in os.listdir(path)]
        self.populate(paths)
        self.setLayout(self.layout)

    def add_image(self, path):
        pixmap = QPixmap()
        if pixmap.load(path):
            pixmap = pixmap.scaled(QSize(200, 200), Qt.AspectRatioMode.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(pixmap)
            self.layout.addWidget(label, self.current_images // self.columns, self.current_images % self.columns)
        self.current_images += 1
    
    def populate(self, paths):
        self.clear()
        for path in paths:
            self.add_image(path)
    
    def clear(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            widget.deleteLater()
        self.current_images = 0