from sqlalchemy.orm import Session

from models.photo_tag import (
    PhotoTag
)


class PhotoTagRepository:

    @staticmethod
    def create(
        db: Session,
        photo_id: str,
        tag_id: str
    ):

        item = PhotoTag(
            photo_id=photo_id,
            tag_id=tag_id
        )

        db.add(item)

        db.commit()

        db.refresh(item)

        return item


    @staticmethod
    def get_by_tag(
        db: Session,
        tag_id: str
    ):

        return (
            db.query(PhotoTag)
            .filter(
                PhotoTag.tag_id == tag_id
            )
            .all()
        )


    @staticmethod
    def delete(
        db: Session,
        photo_id: str,
        tag_id: str
    ):

        item = (
            db.query(PhotoTag)
            .filter(
                PhotoTag.photo_id == photo_id,
                PhotoTag.tag_id == tag_id
            )
            .first()
        )

        if not item:
            return None

        db.delete(item)

        db.commit()

        return item