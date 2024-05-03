from run_mPLUG import run_mPLUG
from run_CLIP import run_CLIP
from run_GPT4 import run_GPT4
from run_GPT4_impl2 import run_GPT4_impl2
from save_image import insert_image
import os
import shutil
import re

# Function to label cropped images

def labelling_mplug(name, asset_type, image):
    images_cropped = "output/" + (image.split('/')[-1]).split('.')[0] + "/cropped/"
    images_unlabelled = "output/" + (image.split('/')[-1]).split('.')[0] + "/unlabelled/"
    images_labelled = "output_mplug/" + (image.split('/')[-1]).split('.')[0]  + "/labelled/"

    # Create empty list to store labels
    labels = []

    for filename in os.listdir(images_cropped):
        if filename.endswith((".jpg", ".jpeg", ".png")):  # Filter only image files
            image_path = os.path.join(images_cropped, filename)

            prompt = """
            I will provide a cropped part of a UV mapping (a 2D representation of a 3D asset) that represents a
            """ + name + """. The object part that appears in the images is from this """ + asset_type + """. Your task is 
            to analyze this cropped image containing the object part, and, taking into account the type of asset, provide a 
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

    



# Function to label cropped images with CLIP

def labelling_clip(name, image, parts):
    images_cropped = "output/" + (image.split('/')[-1]).split('.')[0] + "/cropped/"
    images_unlabelled = "output/" + (image.split('/')[-1]).split('.')[0] + "/unlabelled/"
    images_labelled = "output_clip/" + (image.split('/')[-1]).split('.')[0]  + "/labelled/"

    # Create empty list to store labels
    labels = []

    for filename in os.listdir(images_cropped):
        if filename.endswith((".jpg", ".jpeg", ".png")):  # Filter only image files
            image_path = os.path.join(images_cropped, filename)

            output = run_CLIP(image_path, parts, name)

            label = output

            labels.append(label)

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


# Function to label cropped images with GPT-4

def labelling_gpt4(name, asset_type, image):
    images_cropped = "output/" + (image.split('/')[-1]).split('.')[0] + "/cropped/"
    images_unlabelled = "output/" + (image.split('/')[-1]).split('.')[0] + "/unlabelled/"
    images_labelled = "output_gpt4/" + (image.split('/')[-1]).split('.')[0]  + "/labelled/"

    # Create empty list to store labels
    labels = []

    for filename in os.listdir(images_cropped):
        if filename.endswith((".jpg", ".jpeg", ".png")):  # Filter only image files
            image_path = os.path.join(images_cropped, filename)

            prompt = """
            I will provide a cropped part of a UV mapping (a 2D representation of a 3D asset) that represents a
            """ + name + """. The object part that appears in the images is from this """ + asset_type + """. Your task is 
            to analyze this cropped image containing the object part, and, taking into account the type of asset, provide a 
            label for this part. Please provide this part as a string within "", with no more words. Take a deep 
            breath, and think carefully your answer based on the image provided.
            """


            output = run_GPT4(image_path, prompt)

            # Define pattern for matching object part names
            pattern = r'is a (.*?)\.'

            # Extract object part names using regular expression
            object_parts = re.findall(pattern, output)

            print(object_parts)
            
            if object_parts:
                label = object_parts[0].strip('>').strip('<')
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




def labelling_gpt4_impl2(name, asset_type, image_all):
    images_cropped = "output/" + (image_all.split('/')[-1]).split('.')[0] + "/cropped/"
    images_unlabelled = "output/" + (image_all.split('/')[-1]).split('.')[0] + "/unlabelled/"
    images_labelled = "output_mplug/" + (image_all.split('/')[-1]).split('.')[0]  + "/labelled/"

    # Create empty list to store labels
    labels = []

    for filename in os.listdir(images_cropped):
        if filename.endswith((".jpg", ".jpeg", ".png")):  # Filter only image files
            image_path = os.path.join(images_cropped, filename)

            prompt = """
            I will provide two images. The first one will represent a UV Mapping (a 2D representation of a 3D asset) of a 
            videogame asset that represents a """ + name + """. The second image will represent a cropped part of that UV 
            mapping representing one of its parts. The object part that appears in the image is from this """ + asset_type + """. 
            Your task is to analyze the cropped image containing the object part taking also into account the image that 
            represents the whole asset, and, knowing type of asset, provide a label for this part (the one in the cropped 
            image). Please provide this part as a string within "", with no more words. Take a deep breath, and think 
            carefully your answer based on the images provided.
            """


            output = run_GPT4_impl2(image_all, image_path, prompt)


            # Define pattern for matching object part names
            pattern = r'is a (.*?)\.'

            # Extract object part names using regular expression
            object_parts = re.findall(pattern, output)

            print(object_parts)
            
            if object_parts:
                label = object_parts[0].strip('"').strip('`')
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
