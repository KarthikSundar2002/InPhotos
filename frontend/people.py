from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QRect

import cv2
class People(QLabel):
    def __init__(self, path, size=256):
        super().__init__()
        self.path = path
        self.pixmap = QPixmap(path)
        self.setPixmap(self.pixmap)


    
    