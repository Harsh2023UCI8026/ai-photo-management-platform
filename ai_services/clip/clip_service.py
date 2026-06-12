from transformers import CLIPProcessor
from transformers import CLIPModel

from PIL import Image

import torch


class ClipService:

    model = None
    processor = None

    @classmethod
    def load_model(cls):

        if cls.model is None:

            cls.model = (
                CLIPModel.from_pretrained(
                    "openai/clip-vit-base-patch32"
                )
            )

            cls.processor = (
                CLIPProcessor.from_pretrained(
                    "openai/clip-vit-base-patch32"
                )
            )

    @classmethod
    def generate_embedding(
        cls,
        image_path: str
    ):

        cls.load_model()

        image = (
            Image.open(image_path)
            .convert("RGB")
        )

        inputs = cls.processor(
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():

            features = (
                cls.model.get_image_features(
                    **inputs
                )
            )

        embedding = (
            features[0]
            .cpu()
            .numpy()
            .tolist()
        )

        return embedding