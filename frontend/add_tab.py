import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QProgressBar, QSpacerItem, QSizePolicy
from frontend.group_cluster import ClusterGroup
from image_helpers import batch_image_encode,generate_facial_embeddings

class AddTab(QWidget):
    def __init__(self, image_processor, vec_db, model, facial_model):
        super().__init__()
        self.cluster_paths = []
        self.person_ids = []
        self.image_processor = image_processor
        self.vec_db = vec_db
        self.model = model
        self.facial_model = facial_model
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Directory of Images To Add")
        self.inp = QLineEdit()
        self.inp.setPlaceholderText("Enter the Path to your Folder of Images")
        self.encode_button = QPushButton("ADD IMAGES")
        self.people_button = QPushButton("Find People")
        self.pbar = QProgressBar()
        print("AddTab")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.inp)
        self.layout.addWidget(self.pbar)
        self.layout.addWidget(self.encode_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.people_label = QLabel("People")
        self.people = ClusterGroup(self.vec_db)
        self.layout.addWidget(self.people_label)
        self.layout.addWidget(self.people)
        self.layout.addWidget(self.people_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.layout)
        
        self.layout.insertSpacerItem(6, QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setLayout(self.layout)
    
        self.encode_button.clicked.connect(self.encode_signal)
        self.people_button.clicked.connect(self.find_people_signal)

    def encode_signal(self):
        image_path = self.inp.text()
        paths = [image_path + "/" + path for path in os.listdir(image_path)]
        results = batch_image_encode(image_path, self.model, self.image_processor)
        for i in range(len(paths)):
            facial_embeddings, aligned_faces, pps = generate_facial_embeddings(paths[i], self.facial_model)
            self.vec_db.add(paths[i], results[i], facial_embeddings, aligned_faces, pps)
            self.pbar.setValue(int((i+1)/len(paths)*100))
        print("Added All Entries in DB")
    
    def find_people_signal(self):
        self.find_cluster_paths()
        for i in range(len(self.cluster_paths)):
            self.people.add_cluster(self.cluster_paths[i], self.person_ids[i])

    def find_cluster_paths(self):
        people = self.vec_db.get_people()
        cluster_paths = []
        peep_ids = []
        for person in people:
            if person.name == "Unknown":
                cluster_paths.append(person.face_path)
                peep_ids.append(person.id)
            if len(cluster_paths) == 3:
                break
        print("Cluster Paths:")
        print(cluster_paths)
        print("Peep IDs:")
        print(peep_ids)
        self.cluster_paths = cluster_paths
        self.person_ids = peep_ids