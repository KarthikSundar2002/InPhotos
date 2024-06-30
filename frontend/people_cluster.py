from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QRect
import os

from frontend.people import People

class People_Cluster(QWidget):
    def __init__(self, face_path, id,vec_db, size=256):
        super().__init__()
        self.face_path = face_path
        self.peep_id = id
        self.layout = QHBoxLayout()
        self.outer_layout = QVBoxLayout()
        self.translation = [-20,0,20]
        self.vec_db = vec_db
        i = 0
        for face in os.listdir(self.face_path):
            people = People(self.face_path + face, size)
            print(face)
            self.layout.addWidget(people)
            people.move(people.pos().x() + self.translation[i], people.pos().y())
        self.img_widget = QWidget()
        self.img_widget.setLayout(self.layout)
        self.outer_layout.addWidget(self.img_widget)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter Name")
        self.outer_layout.addWidget(self.line_edit)
        self.setLayout(self.outer_layout)  
    
    def add_name(self):
        name = self.line_edit.text()
        
        self.vec_db.add_name(name, self.peep_id)
        self.line_edit.clear()
        self.line_edit.setPlaceholderText("Enter Name")
        self.line_edit.update()
        print("Added Name")
        
    
    