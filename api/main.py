from flask_restful import Api, Resource, reqparse
from flask import Flask, send_from_directory,current_app,jsonify,request
import requests as req
import numpy as np
import json
from PIL import Image  
from io import BytesIO
# from huggingface_hub import from_pretrained_keras

# model = from_pretrained_keras("MissingBreath/recycle-garbage-model")

# import tensorflow as tf

# model=tf.keras.models.load_model('api/_9217')

# import torchvision.transforms as transforms
# import torch
# import pickle
# from functools import partial
# pickle.load = partial(pickle.load, encoding="latin1")
# pickle.Unpickler = partial(pickle.Unpickler, encoding="latin1")
# model_path = "api/MobileNet__.pth" 
# model = torch.load(model_path, map_location=lambda storage, loc: storage, pickle_module=pickle)
# model = torch.load(model_path)

# image = Image.open("/kaggle/input/garbage-classification/Garbage classification/Garbage classification/cardboard/cardboard1.jpg")  # Change "path_to_your_image.jpg" to the actual file path

# preprocess = transforms.Compose([
#     transforms.Resize(256),
#      transforms.ToTensor()
# ])    

# img = preprocess(image)
# img = img.unsqueeze(0)

# res = model(img)

def pred(test_image):
    # test_image = Image.open(img_path)
    test_image = test_image.resize((128, 128)) 
    test_image = np.array(test_image) / 255.0  
    test_image = np.expand_dims(test_image, axis=0)
    print("pred")
    res=model.predict(test_image[:,:,:,:3])
    print("done")
    res = list(res[0])
    idx=res.index(max(res))
    # cls = ["battery","biological",'brown-glass','cardboard','clothes','green-glass','metal','paper','plastic','shoes','trash','white-glass']
    return idx

import base64

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

from random import randrange

def upload_file(file, url="http://localhost:8000/classify"):
    """
    Uploads a file to the FastAPI endpoint specified by the URL.

    Args:
        file_path (str): The path to the file to upload.
        url (str, optional): The URL of the FastAPI endpoint. Defaults to "http://localhost:8000/classify".

    Returns:
        dict: The response from the FastAPI endpoint.
    """ 
    with BytesIO() as buf:
      file.save(buf, 'jpeg')
      image_bytes = buf.getvalue()

      files = {"image": image_bytes}
      response = req.post(url, files=files)

    return response.json()

class Recycle(Resource):
    def get(self):
        return {
        'message': "recycle Get"
        }

    def post(self):
        print(self)
        
        # matrix_2 = np.array(request.json["matrix2"])
        # print("iam here")
        # # context = request.args.getlist('context')[0]
        # context = ""
        # # image =  request.json["image"]
        res =  request.json["files"]


        # files = request.files["img"]
        # # file = files.get('img')
        # file = request.files["img"]
        # print("iam here")
        # res = file.read()
        # # print(res)
        # # Path to your image
        # # image_path = "path_to_your_image.jpg"

        # # # Getting the base64 string
        # # base64_image = encode_image(image_path)
        img = Image.open(BytesIO(base64.b64decode(res))).convert("RGB")
        # # print("iam here")
        # prediction=-1
        # try:
        #     prediction = pred(im)
        # except:
        #     print("error")
        # print("iam here")
        # response = flask.jsonify({'output': 'prediction'})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # if(prediction == -1):
        #     print("error")
        url = "https://seyf1elislam-test-test.hf.space/classify"
        # response = upload_file(img,url)
        # prediction = response["prediction"]
        try:
            response = upload_file(img,url)
            prediction = response["prediction"]
        except:
            print("error")
            prediction = randrange(12)
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