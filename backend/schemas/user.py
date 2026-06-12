from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    google_id: str | None = None


class UserResponse(BaseModel):
    id: str
    email: str
    google_id: str | None = None

    class Config:
        from_attributes = True