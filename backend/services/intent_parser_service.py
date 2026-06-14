class IntentParserService:

    CATEGORY_WORDS = [
        "food",
        "animal",
        "nature",
        "document",
        "vehicle",
        "building",
        "person",
        "screenshot"
    ]

    @staticmethod
    def detect(
        query: str
    ):

        q = query.lower()

        for category in (
            IntentParserService.CATEGORY_WORDS
        ):

            if category in q:

                return {
                    "type": "category",
                    "value": category
                }

        if (
            "text" in q
            or
            "contains" in q
        ):

            return {
                "type": "ocr",
                "value": query
            }

        return {
            "type": "semantic",
            "value": query
        }