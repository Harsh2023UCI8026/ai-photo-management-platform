from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from models.user import User
from models.photo import Photo

from models.search_history import SearchHistory

from api.photos import router as photos_router
from api.users import router as users_router
from api.auth import router as auth_router
from database.session import SessionLocal

from services.faiss_index_service import (
    FaissIndexService
)

from ai_services.faiss.faiss_service import (
    faiss_service
)

app = FastAPI(
    title="AI Photo Management Platform"
)


@app.on_event("startup")
def startup_event():

    db = SessionLocal()

    try:

        FaissIndexService.load_all_embeddings(
            db
        )

    finally:

        db.close()

# Routers
app.include_router(users_router)
app.include_router(photos_router)
app.include_router(auth_router)

# Static Files (Uploaded Images)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


@app.get("/")
def root():
    return {
        "message": "AI Photo Management Platform Running"
    }