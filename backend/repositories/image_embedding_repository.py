from sqlalchemy.orm import Session

from models.image_embedding import ImageEmbedding

from models.photo import Photo


class ImageEmbeddingRepository:

    @staticmethod
    def create(
        db: Session,
        photo_id: str,
        embedding: list,
        model_name: str
    ):

        db_embedding = ImageEmbedding(
            photo_id=photo_id,
            embedding=embedding,
            model_name=model_name
        )

        db.add(db_embedding)
        db.commit()
        db.refresh(db_embedding)

        return db_embedding

    @staticmethod
    def get_by_photo_id(
        db: Session,
        photo_id: str
    ):

        return (
            db.query(ImageEmbedding)
            .filter(
                ImageEmbedding.photo_id == photo_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(ImageEmbedding)
            .all()
        )
    

    @staticmethod
    def get_all_for_user(
        db: Session,
        user_id: str
    ):

        from models.photo import Photo
        return (
            db.query(ImageEmbedding)
            .join(
                Photo,
                ImageEmbedding.photo_id == Photo.id
            )
            .filter(
                Photo.user_id == user_id
            )
            .all()
        )
    


     