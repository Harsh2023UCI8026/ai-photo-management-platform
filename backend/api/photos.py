import os
from pathlib import Path
import mimetypes
from models.photo import Photo
from fastapi import Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.tasks.photo_tasks import (
    generate_thumbnail
)

from services.search_suggestion_service import (
    SearchSuggestionService
)

from repositories.face_repository import (
    FaceRepository
)

from repositories.face_cluster_repository import (
    FaceClusterRepository
)

from services.face_clustering_service import (
    FaceClusteringService
)

from ai_services.face_recognition.face_service import (
    FaceService
)

from ai_services.clip.clip_service import ClipService

from services.faiss_index_service import (
    FaissIndexService
)

from repositories.image_embedding_repository import (
    ImageEmbeddingRepository
)

from ai_services.classification.classification_service import (
    ClassificationService
)

from repositories.category_repository import (
    CategoryRepository
)

from ai_services.ocr.ocr_service import (
    OCRService
)

from repositories.photo_ocr_repository import (
    PhotoOCRRepository
)

clip_service = ClipService()


from core.dependencies import get_current_user
from fastapi import HTTPException
from core.photo_security import verify_photo_owner


from repositories.image_embedding_repository import ImageEmbeddingRepository
from services.semantic_search_service import SemanticSearchService
from services.ai_search_service import (
    AISearchService
)

from services.smart_search_service import (
    SmartSearchService
)
from repositories.search_history_repository import (
    SearchHistoryRepository
)
from repositories.photo_repository import PhotoRepository
from repositories.photo_ocr_repository import (
    PhotoOCRRepository
)
from ai_services.faiss.faiss_service import (
    faiss_service
)
 


from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from sqlalchemy.orm import Session

from database.session import get_db

from repositories.photo_repository import PhotoRepository
from schemas.photo import PhotoCreate

from schemas.face_cluster import (
    ClusterLabelUpdate
)
from services.photo_service import PhotoService


from services.dashboard_service import (
    DashboardService
)

from services.faiss_index_service import (
    FaissIndexService
)

clip_service = ClipService()




router = APIRouter(
    prefix="/photos",
    tags=["Photos"]
)

class RenamePhoto(BaseModel):
    filename: str


@router.post("/")
def create_photo(
    photo: PhotoCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return PhotoRepository.create(db, photo)


@router.get("/")
def get_photos(
    page: int = 1,
    limit: int = 10,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = current_user["sub"]
    offset = (page - 1) * limit

    photos = (
        db.query(Photo)
        .filter(
            Photo.user_id == user_id,
            Photo.is_deleted == False
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = (
        db.query(Photo)
        .filter(
            Photo.user_id == user_id,
            Photo.is_deleted == False
        )
        .count()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "photos": photos
    }


@router.post("/upload")
async def upload_photo(
     
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["sub"]
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_bytes = await file.read()

    md5_hash = PhotoService.calculate_md5(
        file_bytes
    )

    sha256_hash = PhotoService.calculate_sha256(
        file_bytes
    )

    # Duplicate check
    existing_photo = PhotoRepository.is_duplicate(
        db,
        sha256_hash
    )

    if existing_photo:
        return {
            "message": "Photo already exists",
            "photo_id": existing_photo.id,
            "filename": existing_photo.filename
        }

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(file_bytes)

    width, height = PhotoService.get_dimensions(
        str(file_path)
    )

    hashes = (
        PhotoService.generate_perceptual_hashes(
            str(file_path)
        )
    )



    similar_photo, similarity = (
        PhotoRepository.find_most_similar_photo(
            db,
            hashes["phash"],
            hashes["dhash"],
            hashes["ahash"]
        )
    )

    duplicate_warning = None

    if (
        similar_photo
        and similarity >= 95
    ):
        duplicate_warning = {
            "photo_id": similar_photo.id,
            "filename": similar_photo.filename,
            "similarity": similarity
        }

    db_photo = (PhotoRepository.create_uploaded_photo(
        db=db,
        user_id=user_id,
        filename=file.filename,
        file_path=f"/uploads/{file.filename}",
        thumbnail_path=f"/thumbnails/thumb_{file.filename}",
        file_size=len(file_bytes),
        md5_hash=md5_hash,
        sha256_hash=sha256_hash,
        width=width,
        height=height,
        phash=hashes["phash"],
        dhash=hashes["dhash"],
        ahash=hashes["ahash"])
    
    )

    try:

        embedding = (
            clip_service.generate_embedding(
                str(file_path)
            )
        )

        face_embedding = (
            FaceService.fake_embedding()
        )

        FaceRepository.create(
            db=db,
            photo_id=db_photo.id,
            embedding=face_embedding
        )

        ImageEmbeddingRepository.create(
            db=db,
            photo_id=db_photo.id,
            embedding=embedding,
            model_name="clip-vit-base-patch32"
        )


        FaissIndexService.add_embedding(
            embedding,
            db_photo.id
        )

        print(
            "FAISS UPDATED:",
            db_photo.filename
        )

        classification = (
            ClassificationService.classify(
                str(file_path)
            )
        )

        CategoryRepository.create(
            db=db,
            photo_id=db_photo.id,
            category_name=classification[
                "category"
            ],
            confidence_score=classification[
                "confidence"
         ]
        )

        print(
            "CATEGORY:",
            classification["category"]
        )



        ocr_text = (
            OCRService.extract_text(
                str(file_path)
            )
        )

        if ocr_text:

            PhotoOCRRepository.create(
                db=db,
                photo_id=db_photo.id,
                ocr_text=ocr_text
            )

            print(
                "OCR TEXT:",
                ocr_text[:100]
            )

    except Exception as e:

        print(
            "CLIP ERROR:",
            str(e)
        )


    generate_thumbnail.delay(
    file.filename
    )  

    return {
        "message": "Photo uploaded",
        "photo_id": db_photo.id,
        "user_id": db_photo.user_id,
        "filename": db_photo.filename,
        "file_size": db_photo.file_size,
        "width": db_photo.width,
        "height": db_photo.height,
        "duplicate_warning": duplicate_warning
    }



@router.get("/health")
def health():
    return {
        "api": "healthy"
    }





@router.get("/search")
def search_photos(
    filename: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    photos = (
        db.query(Photo)
        .filter(
            Photo.user_id == current_user["sub"],
            Photo.is_deleted == False,
            Photo.filename.ilike(f"%{filename}%")
        )
        .all()
    )
    return photos




@router.get("/stats")
def stats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):


    photos = (
        db.query(Photo)
        .filter(
            Photo.user_id == current_user["sub"],
            Photo.is_deleted == False
        )
        .all()
    )

     

    total_photos = len(photos)

    total_storage = sum(
        photo.file_size
        for photo in photos
    )

    average_size = (
        total_storage / total_photos
        if total_photos > 0
        else 0
    )

     

    return {
        "total_photos": total_photos,
        "total_storage_bytes": total_storage,
        "average_file_size_bytes": average_size
    }





@router.get("/view/{photo_id}")
def view_photo(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        return {
            "message": "Photo not found"
        }

    verify_photo_owner(
    photo,
    current_user["sub"]
    )

    file_path = photo.file_path.lstrip("/")

    media_type, _ = mimetypes.guess_type(
        file_path
    )

    return FileResponse(
        path=file_path,
        media_type=media_type
    )





@router.get("/download/{photo_id}")
def download_photo(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("DOWNLOAD ID:", photo_id)

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    print("PHOTO:", photo)

    if not photo:
        return {"message": "Photo not found"}

    verify_photo_owner(
    photo,
    current_user["sub"]
    )

    file_path = photo.file_path.lstrip("/")

    print("PATH:", file_path)

    return FileResponse(
        path=file_path,
        filename=photo.filename,
        media_type="application/octet-stream"
    )



@router.get("/{photo_id}/thumbnail")
def get_thumbnail(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    verify_photo_owner(
    photo,
    current_user["sub"]
    )

    thumbnail_path = (
        f"thumbnails/thumb_{photo.filename}"
    )

    if not os.path.exists(thumbnail_path):
        raise HTTPException(
            status_code=404,
            detail="Thumbnail not found"
        )

    return FileResponse(
        path=thumbnail_path,
        filename=f"thumb_{photo.filename}",
        media_type="image/png"
    )


@router.get("/{photo_id}/metadata")
def photo_metadata(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        return {
            "message": "Photo not found"
        }

    verify_photo_owner(
    photo,
    current_user["sub"]
    )

    return {
        "id": photo.id,
        "filename": photo.filename,
        "file_path": photo.file_path,
        "thumbnail_path": photo.thumbnail_path,
        "file_size": photo.file_size,
        "width": photo.width,
        "height": photo.height,
        "md5_hash": photo.md5_hash,
        "sha256_hash": photo.sha256_hash,
        "source_type": photo.source_type,
        "user_id": photo.user_id
    }



@router.put("/{photo_id}/rename")
def rename_photo(
    photo_id: str,
    data: RenamePhoto,
    
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        return {
            "message": "Photo not found"
        }


    verify_photo_owner(
    photo,
    current_user["sub"]
    )

    photo.filename = data.filename

    db.commit()
    db.refresh(photo)

    return {
        "message": "Photo renamed successfully",
        "photo": photo
    }



@router.get("/trash")
def get_trash(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photos = (
        db.query(Photo)
        .filter(
            Photo.user_id == current_user["sub"],
            Photo.is_deleted == True
        )
        .all()
    )

    return {
        "total": len(photos),
        "photos": photos
    }



@router.post("/{photo_id}/restore")
def restore_photo(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    verify_photo_owner(
        photo,
        current_user["sub"]
    )

    photo.is_deleted = False

    db.commit()
    db.refresh(photo)

    return {
        "message": "Photo restored successfully",
        "filename": photo.filename
    }




@router.get("/semantic-search")
def semantic_search(
    query: str,
    limit: int = 10,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    SearchHistoryRepository.create(
        db=db,
        user_id=current_user["sub"],
        query=query
    )

    return (
        SemanticSearchService.search(
            db=db,
            query=query,
            user_id=current_user["sub"],
            limit=limit
        )
    )




@router.get(
    "/search-text"
)
def search_text(
    query: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    records = (
        PhotoOCRRepository.search_text(
            db,
            query
        )
    )

    results = []

    for record in records:

        photo = (
            PhotoRepository.get_by_id(
                db,
                record.photo_id
            )
        )

        if not photo:
            continue

        if str(photo.user_id) != str(
            current_user["sub"]
        ):
            continue

        results.append({

            "photo_id":
            photo.id,

            "filename":
            photo.filename,

            "file_path":
            photo.file_path,

            "ocr_preview":
            record.ocr_text[:200]

        })

    return results
  





@router.delete("/{photo_id}/permanent")
def permanent_delete_photo(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    verify_photo_owner(
        photo,
        current_user["sub"]
    )

    # delete original file

    file_path = photo.file_path.lstrip("/")

    if os.path.exists(file_path):
        os.remove(file_path)

    # delete thumbnail

    if photo.thumbnail_path:

        thumbnail_path = (
            photo.thumbnail_path.lstrip("/")
        )

        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

    PhotoRepository.permanent_delete(
        db,
        photo_id
    )

    FaissIndexService.rebuild_index(
        db
    )

    return {
        "message": "Photo permanently deleted",
        "filename": photo.filename
    }
     



@router.delete("/{photo_id}")
def delete_photo(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    verify_photo_owner(
        photo,
        current_user["sub"]
    )

     
    PhotoRepository.delete(
        db,
        photo_id
    )

    FaissIndexService.rebuild_index(
        db
    )

    return {
        "message": "Photo moved to trash",
        "filename": photo.filename
    }



@router.get("/{photo_id}/similar")
def get_similar_photos(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    verify_photo_owner(
        photo,
        current_user["sub"]
    )

    if  not photo.phash or not photo.dhash or not photo.ahash:
        return {
            "message": "No perceptual hash found"
        }
    
    print("REACHED FIND_SIMILAR")

    similar_photos = (
        PhotoRepository.find_similar_photos(
            db,
            photo.id,
            photo.phash,
            photo.dhash,
            photo.ahash
        )
    )

    return similar_photos



@router.get(
    "/category/{category_name}"
)
def get_photos_by_category(
    category_name: str,
    db: Session = Depends(get_db)
):

    categories = (
        CategoryRepository.get_by_category(
            db,
            category_name
        )
    )

    results = []

    for item in categories:

        photo = (
            PhotoRepository.get_by_id(
                db,
                item.photo_id
            )
        )

        if photo:

            results.append({
                "photo_id": photo.id,
                "filename": photo.filename,
                "file_path": photo.file_path,
                "category": item.category_name,
                "confidence":
                item.confidence_score
            })



    return results




@router.post(
    "/faces/cluster"
)
def cluster_faces(
    db: Session = Depends(get_db)
):

    return (
        FaceClusteringService.cluster_faces(
            db
        )
    )



@router.get(
    "/faces/clusters"
)
def get_clusters(
    db: Session = Depends(
        get_db
    )
):

    return (
        FaceClusteringService.get_clusters(
            db
        )
    )




@router.get(
    "/faces/clusters/{cluster_id}"
)
def get_cluster_photos(
    cluster_id: str,
    db: Session = Depends(get_db)
):

    faces = (
        FaceRepository.get_by_cluster(
            db,
            cluster_id
        )
    )

    results = []

    for face in faces:

        photo = (
            PhotoRepository.get_by_id(
                db,
                face.photo_id
            )
        )

        if photo:

            results.append({
                "photo_id": photo.id,
                "filename": photo.filename,
                "file_path": photo.file_path
            })

    return results





@router.put(
    "/faces/clusters/{cluster_id}/label"
)
def update_cluster_label(
    cluster_id: str,
    data: ClusterLabelUpdate,
    db: Session = Depends(get_db)
):

    cluster = (
        FaceClusterRepository.update_label(
            db,
            cluster_id,
            data.label
        )
    )

    if not cluster:

        raise HTTPException(
            status_code=404,
            detail="Cluster not found"
        )

    return {
        "cluster_id": cluster.id,
        "label": cluster.label
    }





@router.get(
    "/person/{name}"
)
def get_person_photos(
    name: str,
    db: Session = Depends(get_db)
):

    cluster = (
        FaceClusterRepository.get_by_label(
            db,
            name
        )
    )

    if not cluster:

        return []

    faces = (
        FaceRepository.get_by_cluster(
            db,
            cluster.id
        )
    )

    results = []

    for face in faces:

        photo = (
            PhotoRepository.get_by_id(
                db,
                face.photo_id
            )
        )

        if photo:

            results.append({
                "photo_id": photo.id,
                "filename": photo.filename,
                "file_path": photo.file_path
            })

    return results




@router.get(
    "/ai-search"
)
def ai_search(
    query: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return (
        AISearchService.search(
            db=db,
            query=query,
            user_id=current_user["sub"]
        )
    )



@router.get(
    "/suggestions"
)
def get_suggestions(
    query: str,
    db: Session = Depends(get_db)
):

    return (
        SearchSuggestionService.get_suggestions(
            db,
            query
        )
    )






@router.get(
    "/search-smart"
)
def search_smart(
    query: str,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return {
        "query": query,
        "results": (
            AISearchService.search(
                db=db,
                query=query,
                user_id=current_user["sub"]
            )
        )
    }





@router.get(
    "/dashboard"
)
def get_stats(
    db: Session = Depends(
        get_db
    )
):

    return (
        DashboardService.get_stats(
            db
        )
    )










@router.get("/{photo_id}")
def get_photo(
    photo_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    photo = PhotoRepository.get_by_id(
        db,
        photo_id
    )

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    verify_photo_owner(
        photo,
        current_user["sub"]
    )

    return photo










