from sqlalchemy.orm import Session

from models.face_cluster import (
    FaceCluster
)


class FaceClusterRepository:

    @staticmethod
    def create(
        db: Session,
        label: str = None
    ):

        cluster = FaceCluster(
            label=label
        )

        db.add(cluster)

        db.commit()

        db.refresh(cluster)

        return cluster

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(FaceCluster)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        cluster_id: str
    ):

        return (
            db.query(FaceCluster)
            .filter(
                FaceCluster.id == cluster_id
            )
            .first()
        )
    



    @staticmethod
    def count_clusters(
        db: Session
    ):

        return (
            db.query(FaceCluster)
            .count()
        )
    





    @staticmethod
    def update_label(
        db: Session,
        cluster_id: str,
        label: str
    ):

        cluster = (
            db.query(FaceCluster)
            .filter(
                FaceCluster.id == cluster_id
            )
            .first()
        )

        if not cluster:
            return None

        cluster.label = label

        db.commit()

        db.refresh(cluster)

        return cluster
    





    @staticmethod
    def get_by_label(
        db: Session,
        label: str
    ):

        return (
            db.query(FaceCluster)
            .filter(
                FaceCluster.label == label
            )
            .first()
        )
    

    