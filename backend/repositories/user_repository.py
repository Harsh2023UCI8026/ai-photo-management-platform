from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate


class UserRepository:

    @staticmethod
    def create(
        db: Session,
        user: UserCreate
    ):

        db_user = User(
            email=user.email,
            google_id=user.google_id
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def create_user(
        db: Session,
        email: str,
        password_hash: str
    ):

        db_user = User(
            email=email,
            password_hash=password_hash
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: str
    ):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def delete(
        db: Session,
        user_id: str
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            return None

        db.delete(user)
        db.commit()

        return True