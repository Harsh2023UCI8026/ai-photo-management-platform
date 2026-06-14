from sqlalchemy.orm import Session

from models.category import Category


class CategoryRepository:

    @staticmethod
    def create(
        db: Session,
        photo_id: str,
        category_name: str,
        confidence_score: float
    ):

        category = Category(
            photo_id=photo_id,
            category_name=category_name,
            confidence_score=confidence_score
        )

        db.add(category)

        db.commit()

        db.refresh(category)

        return category

    @staticmethod
    def get_by_category(
        db: Session,
        category_name: str
    ):

        return (
            db.query(Category)
            .filter(
                Category.category_name
                == category_name
            )
            .all()
        )
    




    @staticmethod
    def get_category_counts(
        db: Session
    ):

        categories = (
            db.query(Category)
            .all()
        )

        counts = {}

        for category in categories:

            name = (
                category.category_name
            )

            counts[name] = (
                counts.get(name, 0) + 1
            )

        return counts
    


    @staticmethod
    def get_all_categories(
        db: Session
    ):

        return (
            db.query(Category)
            .all()
        )