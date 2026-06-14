class QueryNormalizer:

    @staticmethod
    def normalize(
        query: str
    ):

        query = query.lower()

        mapping = {
            "animals": "animal",
            "pets": "animal",
            "pet": "animal",
            "foods": "food",
            "screenshots": "screenshot"
        }

        return mapping.get(
            query,
            query
        )