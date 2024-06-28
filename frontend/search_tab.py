from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt
from image_helpers import text_encode
from frontend.image_grid import ImageGrid

class SearchTab(QWidget):
    def __init__(self, text_tokenizer, vec_db, model):
        super().__init__()

        self.text_tokenizer = text_tokenizer
        self.vec_db = vec_db
        self.model = model

        self.layout = QVBoxLayout(self)
        self.search_label = QLabel("Search Text")
        self.search_inp = QLineEdit()
        self.search_inp.setPlaceholderText("Enter Text to Search")
        self.search_button = QPushButton("Search")
        self.image_grid = ImageGrid()

        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_inp)
        self.layout.addWidget(self.search_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.image_grid)
        self.layout.insertSpacerItem(3, QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.search_button.clicked.connect(self.search_signal)
    
    def search_signal(self):
        text = self.search_inp.text()
        enc = text_encode(text, self.model, self.text_tokenizer)
        results = self.vec_db.search(enc)
        paths = [result["path"] for result in results] 
        self.image_grid.populate(paths)