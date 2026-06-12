import faiss
import numpy as np
import os


class FaissService:

    def __init__(self):

        self.index = None

        self.photo_ids = []

    def build_index(
        self,
        embeddings,
        photo_ids
    ):
        
        self.photo_ids = photo_ids

        vectors = np.array(
            embeddings,
            dtype=np.float32
        )

        faiss.normalize_L2(
            vectors
        )

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(
            vectors
        )

        os.makedirs(
            "indexes",
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            "indexes/faiss.index"
        )



        return self.index

    def search(
        self,
        query_embedding,
        top_k=10
    ):

        vector = np.array(
            [query_embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(
            vector
        )

        scores, indices = (
            self.index.search(
                vector,
                top_k
            )
        )

        return (
            scores[0],
            indices[0]
        )
    

    def get_photo_id(
        self,
        index
    ):

        return self.photo_ids[index]
    


    def add_embedding(
        self,
        embedding,
        photo_id
    ):
        

        if self.index is None:
            return

        vector = np.array(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(
            vector
        )

        self.index.add(
            vector
        )

        self.photo_ids.append(
            photo_id
        )

        faiss.write_index(
            self.index,
            "indexes/faiss.index"
        )



    
    def load_index(
        self
    ):

        if os.path.exists(
            "indexes/faiss.index"
        ):

            self.index = (
                faiss.read_index(
                    "indexes/faiss.index"
                )
            )

            print(
                "FAISS INDEX LOADED"
            )

        else:

            print(
                "FAISS INDEX NOT FOUND"
            )


faiss_service = FaissService()