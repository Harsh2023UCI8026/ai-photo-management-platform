from sqlalchemy.orm import Session

from models.album import Album


class AlbumRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: str,
        name: str
    ):

        album = Album(
            user_id=user_id,
            name=name
        )

        db.add(album)

        db.commit()

        db.refresh(album)

        return album


    @staticmethod
    def get_all(
        db: Session,
        user_id: str
    ):

        return (
            db.query(Album)
            .filter(
                Album.user_id == user_id
            )
            .all()
        )


    @staticmethod
    def get_by_id(
        db: Session,
        album_id: str
    ):

        return (
            db.query(Album)
            .filter(
                Album.id == album_id
            )
            .first()
        )


    @staticmethod
    def delete(
        db: Session,
        album_id: str
    ):

        album = (
            db.query(Album)
            .filter(
                Album.id == album_id
            )
            .first()
        )

        if not album:
            return None

        db.delete(album)

        db.commit()

        return album