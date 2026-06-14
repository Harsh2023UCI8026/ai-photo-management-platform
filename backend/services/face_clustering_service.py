from repositories.face_repository import (
    FaceRepository
)

from repositories.face_cluster_repository import (
    FaceClusterRepository
)


class FaceClusteringService:

    @staticmethod
    def cluster_faces(
        db
    ):

        faces = (
            FaceRepository.get_all(
                db
            )
        )

        if not faces:
            return []

        cluster = (
            FaceClusterRepository.create(
                db,
                label="Person 1"
            )
        )

        for face in faces:

            FaceRepository.update_cluster(
                db,
                face.id,
                cluster.id
            )

        return {
            "cluster_id": cluster.id,
            "faces": len(faces)
        }
    




    @staticmethod
    def get_clusters(
        db
    ):

        clusters = (
            FaceClusterRepository.get_all(
                db
            )
        )

        results = []

        for cluster in clusters:

            faces = (
                FaceRepository.get_by_cluster(
                    db,
                    cluster.id
                )
            )

            results.append({

                "cluster_id":
                cluster.id,

                "label":
                cluster.label,

                "photo_count":
                len(faces)

            })

        return results