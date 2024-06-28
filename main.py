from transformers import  CLIPModel, CLIPImageProcessor, CLIPTokenizer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont


from frontend.ui import MainWindow
from db import DB
import sys, os

app = QApplication(sys.argv)
QFontDatabase.addApplicationFont("./external/Quicksand-VariableFont_wght.ttf")
app.setFont(QFont("Quicksand", 12))
with open('./frontend/style.qss', 'r') as stlf:
    style = stlf.read()
    app.setStyleSheet(style)

is_first_time = True
if os.getenv("INPHOTOS_INIT"):
    print("Not first time")
    is_first_time = False

if is_first_time:
    print("First time")
    # set the path to objectbox
    os.environ["INPHOTOS_DB"] = "./db"
    # download and set the model
    os.environ["INPHOTOS_MODEL"] = "./model/snapshots/vit-32" 
    os.makedirs(os.environ["INPHOTOS_DB"], exist_ok=True)
    with open("./default.json") as a:
        with open(os.environ["INPHOTOS_DB"] + "/objectbox-model.json", "w") as f:
            f.write(a.read())
    os.environ["INPHOTOS_INIT"] = "1"

vec_db = DB(directory=os.environ["INPHOTOS_DB"])

model = CLIPModel.from_pretrained(os.environ["INPHOTOS_MODEL"])
image_processor = CLIPImageProcessor.from_pretrained(os.environ["INPHOTOS_MODEL"])
text_tokenizer = CLIPTokenizer.from_pretrained(os.environ["INPHOTOS_MODEL"])

window = MainWindow(model=model, text_tokenizer=text_tokenizer, vec_db=vec_db, image_processor=image_processor)
window.show()

app.exec()