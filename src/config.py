import os

BASE_MODEL_ID = os.getenv("BASE_MODEL_ID", "stabilityai/stable-diffusion-xl-base-1.0")
REFINER_MODEL_ID = os.getenv(
    "REFINER_MODEL_ID", "stabilityai/stable-diffusion-xl-refiner-1.0"
)
