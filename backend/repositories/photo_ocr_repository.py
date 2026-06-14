from sqlalchemy.orm import Session

from models.photo_ocr_text import (
    PhotoOCRText
)


class PhotoOCRRepository:

    @staticmethod
    def create(
        db: Session,
        photo_id: str,
        ocr_text: str
    ):

        record = PhotoOCRText(
            photo_id=photo_id,
            ocr_text=ocr_text
        )

        db.add(record)

        db.commit()

        db.refresh(record)

        return record


    @staticmethod
    def get_by_photo(
        db: Session,
        photo_id: str
    ):

        return (
            db.query(PhotoOCRText)
            .filter(
                PhotoOCRText.photo_id
                == photo_id
            )
            .first()
        )


    @staticmethod
    def search_text(
        db: Session,
        query: str
    ):

        return (
            db.query(PhotoOCRText)
            .filter(
                PhotoOCRText.ocr_text.ilike(
                    f"%{query}%"
                )
            )
            .all()
        )