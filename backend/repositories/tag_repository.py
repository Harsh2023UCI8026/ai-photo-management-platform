from sqlalchemy.orm import Session

from models.tag import Tag


class TagRepository:

    @staticmethod
    def create(
        db: Session,
        name: str
    ):

        tag = Tag(
            name=name.lower()
        )

        db.add(tag)

        db.commit()

        db.refresh(tag)

        return tag


    @staticmethod
    def get_by_name(
        db: Session,
        name: str
    ):

        return (
            db.query(Tag)
            .filter(
                Tag.name == name.lower()
            )
            .first()
        )


    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(Tag)
            .all()
        )