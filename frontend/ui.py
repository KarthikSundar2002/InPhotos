from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QProgressBar

from frontend.image_grid import ImageGrid
from image_helpers import image_encode, batch_image_encode, text_encode

import os

class MainWindow(QMainWindow):
    def __init__(self, model, text_tokenizer, vec_db, image_processor):
        super().__init__()
        self.vec_db = vec_db
        self.model = model
        self.text_tokenizer = text_tokenizer
        self.image_processor = image_processor
        self.setWindowTitle("InPhotos")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()
        self.label = QLabel("Directory of Images")
        self.inp = QLineEdit()
        encode_button = QPushButton("Encode")
        self.pbar = QProgressBar()
        self.search_label = QLabel("Search Text")
        self.search_inp = QLineEdit()
        search_button = QPushButton("Search")
        layout.addWidget(self.label)
        layout.addWidget(self.inp)
        layout.addWidget(encode_button)
        layout.addWidget(self.pbar)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_inp)
        layout.addWidget(search_button)

        self.image_grid = ImageGrid()
        layout.addWidget(self.image_grid)

        search_button.clicked.connect(self.search_signal)
        encode_button.clicked.connect(self.encode_signal)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def search_signal(self):
        text = self.search_inp.text()
        enc = text_encode(text, self.model, self.text_tokenizer)
        results = self.vec_db.search(enc)
        paths = [result["path"] for result in results] 
        self.image_grid.populate(paths)

    def encode_signal(self):
        image_path = self.inp.text()
        paths = [image_path + "/" + path for path in os.listdir(image_path)]
        results = batch_image_encode(image_path, self.model, self.image_processor)
        for i in range(len(paths)):
            self.vec_db.add(paths[i], results[i])
            self.pbar.setValue(int((i+1)/len(paths)*100))
        print("Added All Entries in DB")
