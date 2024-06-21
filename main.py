from transformers import  CLIPModel, CLIPImageProcessor, CLIPTokenizer
from PyQt6.QtWidgets import QApplication

from frontend.ui import MainWindow
from db import DB
import sys

app = QApplication(sys.argv)

vec_db = DB()

model = CLIPModel.from_pretrained("./model/snapshots/vit-32")
image_processor = CLIPImageProcessor.from_pretrained("./model/snapshots/vit-32")
text_tokenizer = CLIPTokenizer.from_pretrained("./model/snapshots/vit-32")

window = MainWindow(model=model, text_tokenizer=text_tokenizer, vec_db=vec_db, image_processor=image_processor)
window.show()

app.exec()