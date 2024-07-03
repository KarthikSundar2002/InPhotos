import os
from PIL import Image

def image_encode(image_path, model):
    image = Image.open(image_path)
    outputs = model.get_image_embeddings(image)
    return outputs

def batch_image_encode(image_paths, model):
    print(image_paths)
    paths = [image_paths + "/" + path for path in os.listdir(image_paths)]
    images = [Image.open(image_path) for image_path in paths]
    outputs = model.get_image_embeddings(images)
    print(outputs.shape)
    return outputs

def text_encode(text, model):
    outputs = model.get_text_embeddings([text])
    print(outputs.shape)
    return outputs

