from run_mPLUG import run_mPLUG
from save_image import insert_image
import os
import shutil
import re

# Function to label cropped images

def labelling(name, asset_type, image):
    images_cropped = "output/" + (image.split('/')[-1]).split('.')[0] + "/cropped/"
    images_unlabelled = "output/" + (image.split('/')[-1]).split('.')[0] + "/unlabelled/"
    images_labelled = "output/" + (image.split('/')[-1]).split('.')[0]  + "/labelled/"

    # Create empty list to store labels
    labels = []

    for filename in os.listdir(images_cropped):
        if filename.endswith((".jpg", ".jpeg", ".png")):  # Filter only image files
            image_path = os.path.join(images_cropped, filename)

            prompt = """
            I will provide a cropped part of a UV mapping (a 2D representation of a 3D asset) that represents a
            """ + name + """. The object part that appears in the images is from this """ + asset_type + """. Your task is 
            to analyze this cropped image containing the object part, and, taking the account the type of asset, provide a 
            label for this part. Please provide this part as a string within "", with no more words. Take a deep 
            breath, and think carefully your answer based on the image provided.
            """


            output = run_mPLUG(image_path, prompt)


            # Define pattern for matching object part names
            pattern = r'is a (.*?)\.'

            # Extract object part names using regular expression
            object_parts = re.findall(pattern, output)

            print(object_parts)
            
            if object_parts:
                label = object_parts[0].strip('"')
                # Append label to list
                labels.append(label)

            else:
                label = "unknown"

            # Construct destination path with label
            destination_directory = os.path.join(images_labelled)
            os.makedirs(destination_directory, exist_ok=True)

            # Construct destination file path
            destination_path = os.path.join(destination_directory, label + ".png")

            # check if destination_path exists
            if os.path.exists(destination_path):
                # Name conflict, add a number to the filename
                i = 1
                while True:
                    new_destination_path = os.path.join(destination_directory, f"{label}_{i}.png")
                    if not os.path.exists(new_destination_path):
                        destination_path = new_destination_path
                        break
                    i += 1
            # Copy file from source to destination
            image_unlabelled = images_unlabelled + "/" + filename
            # Copy file from source to destination
            shutil.copyfile(image_unlabelled, destination_path)

            insert_image(image_unlabelled, name, label)

    