from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from PIL import Image

class ImageView(QLabel):
    clicked = pyqtSignal()

    def __init__(self, path, resolution=512):
        super().__init__()
        self.path = path
        pixmap = QPixmap()
        self.resolution = resolution
        self.clicked.connect(self.on_click) 
        self.setStyleSheet("border-radius: 10px;")   
        if pixmap.load(path):
            pixmap = pixmap.scaled(QSize(resolution, resolution),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.setPixmap(pixmap)
        else:
            print("Failed to load image at path", path)
    
    def mousePressEvent(self, event: QMouseEvent):
        self.clicked.emit()

    def on_click(self):
        img = Image.open(self.path)
        img.show()
        
    
    