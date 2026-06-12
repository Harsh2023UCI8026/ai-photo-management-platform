from transformers import CLIPProcessor
from transformers import CLIPModel

import torch


class TextClipService:

    def __init__(self):

        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

    def generate_embedding(
        self,
        text: str
    ):

        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():

            features = (
                self.model.get_text_features(
                    **inputs
                )
            )

        return (
            features
            .squeeze()
            .tolist()
        )