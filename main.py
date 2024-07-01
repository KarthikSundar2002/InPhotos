from transformers import  CLIPModel, CLIPImageProcessor, CLIPTokenizer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
import torch
import duckdb

from edgeface.backbones import get_model
from frontend.ui import MainWindow
from duck_db import DB
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

print("Hi")
#vec_db = duckdb.connect("./duckdb/vec.db")
vec_db = DB()
print("Hello")
model = CLIPModel.from_pretrained(os.environ["INPHOTOS_MODEL"])
image_processor = CLIPImageProcessor.from_pretrained(os.environ["INPHOTOS_MODEL"])
text_tokenizer = CLIPTokenizer.from_pretrained(os.environ["INPHOTOS_MODEL"])
print("Clip model loaded")
facial_model_name = 'edgeface_s_gamma_05'
facial_model = get_model(facial_model_name)
checkpoint_path = f'edgeface/checkpoints/edgeface_s_gamma_05.pt'
facial_model.load_state_dict(torch.load(checkpoint_path, map_location='cpu'))
facial_model.eval()
print("Facial model loaded")
window = MainWindow(model=model, text_tokenizer=text_tokenizer, vec_db=vec_db, image_processor=image_processor, facial_model=facial_model)
window.show()

app.exec()