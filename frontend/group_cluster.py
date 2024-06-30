from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from frontend.people_cluster import People_Cluster


class ClusterGroup(QWidget):
    def __init__(self, vec_db):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.button = QPushButton("Add Names")
        self.vec_db = vec_db
        self.button.clicked.connect(self.add_names)
    
    def add_names(self):
        widgets = (self.layout.itemAt(i).widget() for i in range(self.layout.count())) 
        for widget in widgets:
            if isinstance(widget, People_Cluster):
                widget.add_name()

    def add_cluster(self, cluster_path, id):
        cluster = People_Cluster(cluster_path, id,self.vec_db)
        self.layout.addWidget(cluster)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)