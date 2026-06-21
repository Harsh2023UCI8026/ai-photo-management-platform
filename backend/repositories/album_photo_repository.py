from sqlalchemy.orm import Session

from models.album_photo import (
    AlbumPhoto
)


class AlbumPhotoRepository:

    @staticmethod
    def add_photo(
        db: Session,
        album_id: str,
        photo_id: str
    ):

        item = AlbumPhoto(
            album_id=album_id,
            photo_id=photo_id
        )

        db.add(item)

        db.commit()

        db.refresh(item)

        return item


    @staticmethod
    def get_album_photos(
        db: Session,
        album_id: str
    ):

        return (
            db.query(AlbumPhoto)
            .filter(
                AlbumPhoto.album_id
                == album_id
            )
            .all()
        )


    @staticmethod
    def remove_photo(
        db: Session,
        album_id: str,
        photo_id: str
    ):

        item = (
            db.query(AlbumPhoto)
            .filter(
                AlbumPhoto.album_id
                == album_id,

                AlbumPhoto.photo_id
                == photo_id
            )
            .first()
        )

        if not item:
            return None

        db.delete(item)

        db.commit()

        return item