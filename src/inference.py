import os

from huggingface_hub import InferenceClient
from PIL import Image

from src.config import BASE_MODEL_ID, REFINER_MODEL_ID


def generate_image_from_text(huggingface_token: str, full_prompt: str) -> Image.Image:
    tmp_folder_path = "tmp"
    tmp_image_filename = "image.png"
    os.makedirs(tmp_folder_path, exist_ok=True)
    tmp_image_path = os.path.join(tmp_folder_path, tmp_image_filename)
    hf_client = InferenceClient(token=huggingface_token)
    base_image = hf_client.text_to_image(full_prompt, model=BASE_MODEL_ID)
    base_image.save(tmp_image_path, format="PNG")
    refined_image = hf_client.image_to_image(tmp_image_path, model=REFINER_MODEL_ID)
    return refined_image
