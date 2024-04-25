from pymongo import MongoClient
from bson.binary import Binary
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import cv2



# Connect to MongoDB
client = MongoClient("mongodb+srv://prueba:prueba123@cluster0.nvaq2lo.mongodb.net/")
db = client["labeled_masks"]


def insert_image(image_path: str, asset: str, label: str):
    # Collection name
    collection = db[asset]

    new_image = cv2.imread(image_path)

    # Convert the color (OpenCV uses BGR by default) to RGB
    image_rgb = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

    # Convert the numpy array (image) to a PIL Image
    image_pil = Image.fromarray(image_rgb)

    # Save PIL Image to BytesIO object
    image_stream = BytesIO()
    image_pil.save(image_stream, format='PNG')

    # Encode the image as base64
    base64_encoded = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Insert the image into MongoDB with the specified name
    result = collection.insert_one({"name": label, "image": base64_encoded})

    print(f"Image inserted with ObjectID: {result.inserted_id}")