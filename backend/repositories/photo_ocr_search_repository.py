from sqlalchemy.orm import Session

from models.photo_ocr_text import (
    PhotoOCRText
)


class PhotoOCRSearchRepository:

    @staticmethod
    def search(
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