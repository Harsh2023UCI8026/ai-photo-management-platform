from ai_services.clip.clip_service import (
    ClipService
)

from ai_services.clip.text_clip_service import (
    TextClipService
)


text_service = TextClipService()


class ClassificationService:

    CATEGORIES = [
        "animal",
        "person",
        "nature",
        "document",
        "food",
        "vehicle",
        "building",
        "screenshot"
    ]

    @staticmethod
    def classify(image_path: str):

        image_embedding = (
            ClipService.generate_embedding(
                image_path
            )
        )

        best_category = "unknown"
        best_score = -999999

        for category in (
            ClassificationService.CATEGORIES
        ):

            text_embedding = (
                text_service.generate_embedding(
                    category
                )
            )

            score = sum(
                a * b
                for a, b in zip(
                    image_embedding,
                    text_embedding
                )
            )

            if score > best_score:

                best_score = score
                best_category = category

        return {
            "category": best_category,
            "confidence": float(best_score)
        }