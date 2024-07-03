from PyQt6.QtWidgets import QMainWindow, QTabWidget

from frontend.add_tab import AddTab
from frontend.search_tab import SearchTab


class MainWindow(QMainWindow):
    def __init__(self, model, vec_db):
        super().__init__()
        self.vec_db = vec_db
        self.model = model
        print("MainWindow")
        self.setWindowTitle("InPhotos")
        self.setMinimumSize(800, 600)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBarAutoHide(True)
        print("Added TabWidget")
        self.tab_widget.addTab(AddTab(vec_db=self.vec_db, model=self.model), "Add")
        print("Added AddTab")
        self.tab_widget.addTab(SearchTab(vec_db=self.vec_db, model=self.model), "Search Images")
        print("Added SearchTab")
        self.setCentralWidget(self.tab_widget)


    

