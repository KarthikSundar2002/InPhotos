import os
from PIL import Image

from transformers import CLIPModel, CLIPImageProcessor, CLIPTokenizerFast

def image_encode(image_path, model: CLIPModel, image_processor: CLIPImageProcessor):
    image = Image.open(image_path)
    print("Image: " + image_path)
    inputs = image_processor.preprocess(images=image, return_tensors="pt")
    print(inputs)
    outputs = model.get_image_features(**inputs)
    
    return outputs

def batch_image_encode(image_paths, model: CLIPModel, image_processor: CLIPImageProcessor):
    print(image_paths)
    paths = [image_paths + "/" + path for path in os.listdir(image_paths)]
    images = [Image.open(image_path) for image_path in paths]
    inputs = image_processor.preprocess(images=images, return_tensors="pt")
    print("Preprocessing is done")
    outputs = model.get_image_features(**inputs)
    print(outputs.shape)
    return outputs

def text_encode(text, model: CLIPModel, text_processor: CLIPTokenizerFast):
    inputs = text_processor.encode(text, return_tensors="pt")
    outputs = model.get_text_features(inputs)
    print(outputs.shape)
    return outputs