from transformers import  CLIPModel, CLIPImageProcessor, CLIPTokenizer
from PyQt6.QtWidgets import QApplication

from frontend.ui import MainWindow
from db import DB
import sys, os

app = QApplication(sys.argv)


env = os.environ
is_first_time = True
if os.getenv("INPHOTOS_INIT"):
    is_first_time = False

if is_first_time:
    # set the path to objectbox
    env["INPHOTOS_DB"] = "./db"
    # download and set the model
    env["INPHOTOS_MODEL"] = "./model/snapshots/vit-32" 
    os.makedirs(env["INPHOTOS_DB"], exist_ok=True)
    with open("./default.json") as a:
        with open(env["INPHOTOS_DB"] + "/objectbox-model.json", "w") as f:
            f.write(a.read())

vec_db = DB(directory=env["INPHOTOS_DB"])

model = CLIPModel.from_pretrained(env["INPHOTOS_MODEL"])
image_processor = CLIPImageProcessor.from_pretrained(env["INPHOTOS_MODEL"])
text_tokenizer = CLIPTokenizer.from_pretrained(env["INPHOTOS_MODEL"])

window = MainWindow(model=model, text_tokenizer=text_tokenizer, vec_db=vec_db, image_processor=image_processor)
window.show()

app.exec()