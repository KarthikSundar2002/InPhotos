import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QProgressBar, QSpacerItem, QSizePolicy
from image_helpers import batch_image_encode 

class AddTab(QWidget):
    def __init__(self, image_processor, vec_db, model):
        super().__init__()

        self.image_processor = image_processor
        self.vec_db = vec_db
        self.model = model

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Directory of Images To Add")
        self.inp = QLineEdit()
        self.inp.setPlaceholderText("Enter the Path to your Folder of Images")
        self.encode_button = QPushButton("ADD IMAGES")
        self.pbar = QProgressBar()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.inp)
        self.layout.addWidget(self.pbar)
        self.layout.addWidget(self.encode_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.insertSpacerItem(4, QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setLayout(self.layout)
    
        self.encode_button.clicked.connect(self.encode_signal)

    def encode_signal(self):
        image_path = self.inp.text()
        paths = [image_path + "/" + path for path in os.listdir(image_path)]
        results = batch_image_encode(image_path, self.model, self.image_processor)
        for i in range(len(paths)):
            self.vec_db.add(paths[i], results[i])
            self.pbar.setValue(int((i+1)/len(paths)*100))
        print("Added All Entries in DB")