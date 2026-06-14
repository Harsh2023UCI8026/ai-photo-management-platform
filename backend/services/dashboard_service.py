from repositories.photo_repository import (
    PhotoRepository
)

from repositories.face_repository import (
    FaceRepository
)

from repositories.face_cluster_repository import (
    FaceClusterRepository
)

from repositories.category_repository import (
    CategoryRepository
)


class DashboardService:

    @staticmethod
    def get_stats(
        db
    ):

        return {

            "total_photos":
            PhotoRepository.count_all(
                db
            ),

            "total_storage_bytes":
            PhotoRepository.total_storage(
                db
            ),

            "total_faces":
            FaceRepository.count_faces(
                db
            ),

            "total_clusters":
            FaceClusterRepository.count_clusters(
                db
            ),

            "categories":
            CategoryRepository.get_category_counts(
                db
            )
        }