import os
from PIL import Image
import torch
from torchvision import transforms
from edgeface.face_alignment import align
import truecase
import nltk

import numpy as np
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

def generate_facial_embeddings(image_path, facial_model):
    
    transform = transforms.Compose([transforms.ToTensor(),                            
                                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])
    aligned_faces = align.get_aligned_face(image_path)
    test_path = "./test/"
    embeddings = []
    i = 0
    pps = []
    for face in aligned_faces:
        pp = test_path + image_path.split("/")[-1] + str(i) +"aligned_face.jpg"
        face.save(pp)
        transformed = transform(face).unsqueeze(0)
        embedding = facial_model(transformed)
        embeddings.append(embedding)
        pps.append(pp)
        i = i + 1
    # transformeds.append(transformed)
    return embeddings, aligned_faces, pps

def named_entity_recognition(text):
    text = truecase.get_true_case(text)
    ner_results = extract_ne(text)
    return ner_results

def extract_ne(quote):
     words = nltk.word_tokenize(quote)
     tags = nltk.pos_tag(words)
     tree = nltk.ne_chunk(tags, binary=True)
     return set(
         " ".join(i[0] for i in t)
         for t in tree
         if hasattr(t, "label") and t.label() == "NE"
     )

