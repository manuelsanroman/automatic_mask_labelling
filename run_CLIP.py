import os
import torch
import clip
from PIL import Image
import cv2

# Load the CLIP model
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def run_CLIP(img_path, labels, name, threshold=0.5):
    # Process each image
    image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)

    # Process each label
    text_inputs = torch.cat([clip.tokenize(f"a photo of a {name} {label}") for label in labels]).to(device)
    
    # Calculate features
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)

    # Calculate similarities and convert to probabilities
    similarities = image_features @ text_features.T
    probabilities = similarities.softmax(dim=-1)
    
    # Find the highest probability and the corresponding label index
    max_probability, max_index = probabilities.max(dim=-1)
    print('Probabilities:', probabilities)  # For debugging: print all probabilities
    
    # Assign labels
    if max_probability < threshold:
        label = "Unknown"
    else:
        label = labels[max_index]
    
    return label
