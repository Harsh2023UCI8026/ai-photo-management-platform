from repositories.image_embedding_repository import (
    ImageEmbeddingRepository
)

from ai_services.faiss.faiss_service import (
    faiss_service
)


class FaissIndexService:

    @staticmethod
    def load_all_embeddings(
        db
    ):

        embeddings = (
            ImageEmbeddingRepository.get_all(
                db
            )
        )

        if not embeddings:
            return

        embedding_vectors = []
        photo_ids = []

        for item in embeddings:

            embedding_vectors.append(
                item.embedding
            )

            photo_ids.append(
                item.photo_id
            )

        faiss_service.build_index(
            embedding_vectors,
            photo_ids
        )

        print(
            f"FAISS LOADED: {len(photo_ids)} vectors"
        )


    
    @staticmethod
    def add_embedding(
        embedding,
        photo_id
    ):

        faiss_service.add_embedding(
            embedding,
            photo_id
        )

    

    @staticmethod
    def rebuild_index(
        db
    ):

        embeddings = (
            ImageEmbeddingRepository.get_all(
                db
            )
        )

        if not embeddings:

            return

        embedding_vectors = []
        photo_ids = []

        for item in embeddings:

            embedding_vectors.append(
                item.embedding
            )

            photo_ids.append(
                item.photo_id
            )

        faiss_service.build_index(
            embedding_vectors,
            photo_ids
        )

        print(
            f"FAISS REBUILT: {len(photo_ids)} vectors"
        )