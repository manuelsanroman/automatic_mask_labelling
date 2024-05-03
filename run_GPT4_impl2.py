from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def run_GPT4_impl2(image_all, image_part, prompt):

    # Getting the base64 string
    base64_image_all = encode_image(image_all)
    base64_image_part = encode_image(image_part)

    response = client.chat.completions.create(
    model= "gpt-4-turbo",
    messages= [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image_all}"
            },
            },
            {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image_part}",
            },
            },
        ]
        }
    ],
    max_tokens = 300
    )

    choice = response.choices[0]

    content = choice.message.content

    return content