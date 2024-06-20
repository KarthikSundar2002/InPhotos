from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QSize

class ImageView(QLabel):
    def __init__(self, path):
        super().__init__()
        pixmap = QPixmap()
        if pixmap.load(path):
            pixmap = pixmap.scaled(QSize(512, 512),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(pixmap)
        else:
            print("Failed to load image at path", path)