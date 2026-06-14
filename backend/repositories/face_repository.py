from sqlalchemy.orm import Session

from models.face import Face


class FaceRepository:

    @staticmethod
    def create(
        db: Session,
        photo_id: str,
        embedding: list,
        cluster_id: str = None
    ):

        face = Face(
            photo_id=photo_id,
            embedding=embedding,
            cluster_id=cluster_id
        )

        db.add(face)

        db.commit()

        db.refresh(face)

        return face

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(Face)
            .all()
        )
    





    @staticmethod
    def get_by_photo(
        db: Session,
        photo_id: str
    ):

        return (
            db.query(Face)
            .filter(
                Face.photo_id == photo_id
            )
            .all()
        )
    



    @staticmethod
    def update_cluster(
        db: Session,
        face_id: str,
        cluster_id: str
    ):

        face = (
            db.query(Face)
            .filter(
                Face.id == face_id
            )
            .first()
        )

        if not face:
            return None

        face.cluster_id = cluster_id

        db.commit()

        db.refresh(face)

        return face
    




    @staticmethod
    def get_by_cluster(
        db: Session,
        cluster_id: str
    ):

        return (
            db.query(Face)
            .filter(
                Face.cluster_id
                == cluster_id
            )
            .all()
        )
    




    @staticmethod
    def count_faces(
        db: Session
    ):

        return (
            db.query(Face)
            .count()
        )
    



    