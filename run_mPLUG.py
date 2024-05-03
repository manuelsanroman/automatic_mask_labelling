import replicate
import os
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

def run_mPLUG(image, prompt):

    img = open(image, "rb")

    input = {
    "img": img,
    "top_k": 25,
    "prompt": prompt,
    "max_length": 500,
    "penalty_alpha": 0.25,
    "temperature": 0.01
    }

    output = replicate.run(
        "joehoover/mplug-owl:51a43c9d00dfd92276b2511b509fcb3ad82e221f6a9e5806c54e69803e291d6b",
        input=input
    )
    output_text = "".join(output)

    return output_text