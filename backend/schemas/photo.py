from pydantic import BaseModel


class PhotoCreate(BaseModel):
    user_id: str
    filename: str
    file_path: str
    thumbnail_path: str | None = None
    file_size: int
    md5_hash: str
    sha256_hash: str
    width: int
    height: int
    source_type: str


class PhotoResponse(PhotoCreate):
    id: str

    class Config:
        from_attributes = True