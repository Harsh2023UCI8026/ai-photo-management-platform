import numpy as np

from ai_services.clip.text_clip_service import (
    TextClipService
)

from ai_services.faiss.faiss_service import (
    faiss_service
)

from repositories.image_embedding_repository import (
    ImageEmbeddingRepository
)

from repositories.photo_repository import (
    PhotoRepository
)

text_clip_service = TextClipService()


class SemanticSearchService:

    @staticmethod
    def cosine_similarity(
        vector1: list,
        vector2: list
    ):

        v1 = np.array(vector1)
        v2 = np.array(vector2)

        return float(
            np.dot(v1, v2)
            /
            (
                np.linalg.norm(v1)
                *
                np.linalg.norm(v2)
            )
        )

    @staticmethod
    def search(
        db,
        query,
        user_id,
        limit=10
    ):

        query_embedding = (
            text_clip_service.generate_embedding(
                query
            )
        )


        if faiss_service.index is None:

            return []

 

        scores, indices = (
            faiss_service.search(
                query_embedding,
                limit
            )
        )

        results = []

        for score, index in zip(
            scores,
            indices
        ):

            if index == -1:
                continue

            if score < 0.20:
                continue

            photo_id = (
                faiss_service.get_photo_id(
                    index
                )
            )

            photo = (
                PhotoRepository.get_by_id(
                    db,
                    photo_id
                )
            )


            if not photo:
                continue


            if str(photo.user_id) != str(user_id):
                continue

            

            results.append({
                "photo_id": photo.id,
                "filename": photo.filename,
                "thumbnail": photo.thumbnail_path,
                "file_path": photo.file_path,
                "similarity": float(score)
            })

        return results