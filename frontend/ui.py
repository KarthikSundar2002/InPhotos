from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QProgressBar, QTabWidget, QTabBar

from frontend.add_tab import AddTab
from frontend.search_tab import SearchTab

class MainWindow(QMainWindow):
    def __init__(self, model, text_tokenizer, vec_db, image_processor):
        super().__init__()
        self.vec_db = vec_db
        self.model = model
        self.text_tokenizer = text_tokenizer
        self.image_processor = image_processor
        self.setWindowTitle("InPhotos")
        self.setMinimumSize(800, 600)
        # with open("./frontend/style.css") as f:
        #     self.styleSheet = f.read()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBarAutoHide(True)
        self.tab_widget.addTab(AddTab(image_processor=self.image_processor, vec_db=self.vec_db, model=self.model), "Add")
        self.tab_widget.addTab(SearchTab(text_tokenizer=self.text_tokenizer, vec_db=self.vec_db, model=self.model), "Search Images")
        self.setCentralWidget(self.tab_widget)


    

