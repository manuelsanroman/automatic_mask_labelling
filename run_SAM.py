from FastSAM.fastsam import FastSAM, FastSAMPrompt 
import ast
import torch
from PIL import Image
from FastSAM.utils.tools import convert_box_xywh_to_xyxy
import cv2
import os

def run_SAM(img_path, max_value=None):
    model_path = "./FastSAM/weights/FastSAM-x.pt"
    imgsz = 1024
    iou = 0.9
    text_prompt = None
    conf = 0.4
    output = "./output/" + f"{(img_path.split('/')[-1]).split('.')[0]}"
    randomcolor = True
    point_prompt = "[[0,0]]"
    point_label = "[0]"
    box_prompt = "[[0,0,0,0]]"
    better_quality = False
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    retina = True
    withContours = False

    # load model
    model = FastSAM(model_path)
    point_prompt = ast.literal_eval(point_prompt)
    box_prompt = convert_box_xywh_to_xyxy(ast.literal_eval(box_prompt))
    point_label = ast.literal_eval(point_label)
    input = Image.open(img_path).convert("RGB")
    everything_results = model(
        input,
        device=device,
        retina_masks=retina,
        imgsz=imgsz,
        conf=conf,
        iou=iou    
        )
    
    if max_value is not None:
        # Run loop for max_value
        loop_range = range(max_value)
    else:
        # Run loop for i
        loop_range = range(len(everything_results[0]))

    for i in loop_range:
        bboxes = None
        points = None
        point_label = None
        black_image = Image.new("RGB", (input.size[0], input.size[1]), (0, 0, 0))
        prompt_process = FastSAMPrompt(black_image, everything_results[0][i], device=device)
        if box_prompt[0][2] != 0 and box_prompt[0][3] != 0:
                ann = prompt_process.box_prompt(bboxes=box_prompt)
                bboxes = box_prompt
        elif text_prompt != None:
            ann = prompt_process.text_prompt(text=text_prompt)
        elif point_prompt[0] != [0, 0]:
            ann = prompt_process.point_prompt(
                points=point_prompt, pointlabel=point_label
            )
            points = point_prompt
            point_label = point_label
        else:
            ann = prompt_process.everything_prompt()

        output_path = output + "/unlabelled/" + f"{i}_{img_path.split('/')[-1]}"

        prompt_process.plot(
            annotations=ann,
            output_path=output_path,
            bboxes=bboxes,
            points=points,
            point_label=point_label,
            withContours=withContours,
            better_quality=better_quality,
        )
        
        image = cv2.imread(output_path, cv2.IMREAD_GRAYSCALE)
        original_image = cv2.imread(img_path)

        # Threshold the image to create a binary image
        _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        # Find contours of white regions
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cropped_images = []

        # Iterate through contours
        for contour in contours:
            # Get bounding box of contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw bounding box on original image
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Crop the original image based on bounding box
            cropped_image = original_image[y:y+h, x:x+w]

            output_dir = output + "/cropped/"

            os.makedirs(output_dir, exist_ok=True)
            
            # Save the cropped image
            path = output_dir + f"{i}_{img_path.split('/')[-1]}"
            cv2.imwrite(path, cropped_image)
