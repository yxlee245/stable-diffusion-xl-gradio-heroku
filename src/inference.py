import os

from huggingface_hub import InferenceClient
from PIL import Image

from src.config import BASE_MODEL_ID, REFINER_MODEL_ID


def generate_image_from_text(huggingface_token: str, full_prompt: str) -> Image.Image:
    """Generate image from full prompt (concatenated chat history), using SDXL base and refiner models as described in
        Huggingface Model Cards

    Args:
        huggingface_token (str): Huggingface Access Token needed to access SDXL models on Huggingface Hub
        full_prompt (str): Concatenated chat history used as prompt for image generation

    Returns:
        Image.Image: Generated image from the SDXL models
    """
    tmp_folder_path = "tmp"
    tmp_image_filename = "image.png"
    os.makedirs(tmp_folder_path, exist_ok=True)
    tmp_image_path = os.path.join(tmp_folder_path, tmp_image_filename)
    hf_client = InferenceClient(token=huggingface_token)
    base_image = hf_client.text_to_image(full_prompt, model=BASE_MODEL_ID)
    base_image.save(tmp_image_path, format="PNG")
    refined_image = hf_client.image_to_image(tmp_image_path, model=REFINER_MODEL_ID)
    return refined_image
