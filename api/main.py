from flask_restful import Api, Resource, reqparse
from flask import Flask, send_from_directory,current_app,jsonify,request
import requests as req
import numpy as np
import math as mt
import json
from PIL import Image  

from PIL import Image

import torchvision.transforms as transforms
import torch
# import pickle
# from functools import partial
# pickle.load = partial(pickle.load, encoding="latin1")
# pickle.Unpickler = partial(pickle.Unpickler, encoding="latin1")
model_path = "api/MobileNet__.pth" 
# model = torch.load(model_path, map_location=lambda storage, loc: storage, pickle_module=pickle)
model = torch.load(model_path)

# image = Image.open("/kaggle/input/garbage-classification/Garbage classification/Garbage classification/cardboard/cardboard1.jpg")  # Change "path_to_your_image.jpg" to the actual file path

# preprocess = transforms.Compose([
#     transforms.Resize(256),
#      transforms.ToTensor()
# ])    

# img = preprocess(image)
# img = img.unsqueeze(0)

# res = model(img)

def pred(img_path):
    test_image = Image.open(img_path)
    test_image = test_image.resize((128, 128)) 
    test_image = np.array(test_image) / 255.0  
    test_image = np.expand_dims(test_image, axis=0)
    res=model.predict(test_image)
    res=list(res)
    idx=res.index(max(res))
    cls = ["battery","biological",'brown-glass','cardboard','clothes','green-glass','metal','paper','plastic','shoes','trash','white-glass']
    return cls[idx]

class Recycle(Resource):
    def get(self):
        return {
        'message': "recycle Get"
        }

    def post(self):
        print(self)
        
        # matrix_2 = np.array(request.json["matrix2"])

        # context = request.args.getlist('context')[0]
        context = ""
        image =  request.json["image"]
        print(image)

        
        # prediction = model(image)
        prediction = 0
        return {"output":prediction}

API_KEY  = "blBXxEYF7eYX0h3O17rtVZOc0REp0RW6"
class Chat(Resource):
    def get(self):
        return {
        'message': "chat Get"
        }

    def post(self):
        print(self)
        
        # matrix_2 = np.array(request.json["matrix2"])

        # context = request.args.getlist('context')[0]
        context = ""
        question =  request.json["question"]

        url = "https://api.ai21.com/studio/v1/j2-ultra/chat"
        
        payload = {
            "numResults": 1,
            "temperature": 0.7,
            "messages": [
                {
                    "text": question,
                    "role": "user"
                }
            ],
            "system": "You are an AI assistant for recycling garbage. Your responses should be informative and concise."

        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f'Bearer {API_KEY}'
        }

        response = req.post(url, json=payload, headers=headers)

        data = json.loads(response.text)
        
        return {"output":data["outputs"][0]["text"]}