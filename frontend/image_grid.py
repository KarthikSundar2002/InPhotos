from PyQt6.QtWidgets import QWidget, QGridLayout

from frontend.image import ImageView

class ImageGrid(QWidget):
    def __init__(self, path="/home/stark/test"):
        super().__init__()
        self.layout = QGridLayout()
        self.columns = 4
        self.current_images = 0
        self.dir_path = path
        self.setLayout(self.layout)

    def add_image(self, path):
        img = ImageView(path)
        self.layout.addWidget(img, self.current_images // self.columns, self.current_images % self.columns)
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