import hashlib
from pathlib import Path

from PIL import Image
import imagehash

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class PhotoService:

    @staticmethod
    def calculate_md5(file_bytes: bytes):
        return hashlib.md5(file_bytes).hexdigest()

    @staticmethod
    def calculate_sha256(file_bytes: bytes):
        return hashlib.sha256(file_bytes).hexdigest()

    @staticmethod
    def get_dimensions(file_path: str):

        with Image.open(file_path) as image:
            return image.width, image.height
    
    @staticmethod
    def generate_perceptual_hashes(
        file_path: str
    ):

        with Image.open(file_path) as image:

            return {
                "phash": str(
                    imagehash.phash(image)
                ),

                "dhash": str(
                    imagehash.dhash(image)
                ),

                "ahash": str(
                    imagehash.average_hash(image)
                )
            }
    

    @staticmethod
    def hash_distance(
        hash1: str,
        hash2: str
    ):

        return bin(
            int(hash1, 16)
            ^
            int(hash2, 16)
        ).count("1")
    

    @staticmethod
    def similarity_percentage(
        hash1: str,
        hash2: str
    ):

        distance = (
            PhotoService.hash_distance(
                hash1,
                hash2
            )
        )

        return round(
            (
                (64 - distance)
                / 64
            ) * 100,
            2
        )
    



    @staticmethod
    def combined_similarity(
        phash1: str,
        phash2: str,
        dhash1: str,
        dhash2: str,
        ahash1: str,
        ahash2: str
    ):

        phash_score = (
            PhotoService.similarity_percentage(
                phash1,
                phash2
            )
        )

        dhash_score = (
            PhotoService.similarity_percentage(
                dhash1,
                dhash2
            )
        )

        ahash_score = (
            PhotoService.similarity_percentage(
                ahash1,
                ahash2
            )
        )

        final_score = (
            phash_score * 0.4
            +
            dhash_score * 0.3
            +
            ahash_score * 0.3
        )

        return round(final_score, 2)