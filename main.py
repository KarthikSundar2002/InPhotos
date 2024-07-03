
from onnx_clip import OnnxClip
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont, QIcon
from PyQt6.QtCore import QSettings
from frontend.ui import MainWindow
#from duck_db import DB
from db import DB
import sys, os

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'Karthik.InPhotos.1.0.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

app = QApplication(sys.argv)
QFontDatabase.addApplicationFont("./external/Quicksand-VariableFont_wght.ttf")
app.setFont(QFont("Quicksand", 12))
app.setWindowIcon(QIcon("./picture.ico"))
with open('./frontend/style.qss', 'r') as stlf:
    style = stlf.read()
    app.setStyleSheet(style)
settings = QSettings("Karthik's Apps", "InPhotos")

is_first_time = False

if settings.value("first_time") is None:
    is_first_time = True

if is_first_time:
    os.makedirs("./db", exist_ok=True)
    settings.setValue("first_time", True)

print("First Time: " + str(is_first_time))
print("Hi")
#vec_db = DB(is_first_time)
vec_db = DB(directory="./db")
print("Hello")
model = OnnxClip(batch_size=32)
print("Clip model loaded")
window = MainWindow(model=model, vec_db=vec_db)
window.show()

app.exec()