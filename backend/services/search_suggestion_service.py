from repositories.category_repository import (
    CategoryRepository
)

from repositories.face_cluster_repository import (
    FaceClusterRepository
)


class SearchSuggestionService:

    @staticmethod
    def get_suggestions(
        db,
        query: str
    ):

        q = query.lower()

        suggestions = set()

        #
        # categories
        #

        categories = (
            CategoryRepository.get_all_categories(
                db
            )
        )

        for item in categories:

            if (
                item.category_name.lower()
                .startswith(q)
            ):

                suggestions.add(
                    item.category_name
                )

        #
        # people
        #

        clusters = (
            FaceClusterRepository.get_all(
                db
            )
        )

        for cluster in clusters:

            if (
                cluster.label
                and
                cluster.label.lower()
                .startswith(q)
            ):

                suggestions.add(
                    cluster.label
                )

        return sorted(
            list(suggestions)
        )