import numpy as np


class FaceService:

    @staticmethod
    def fake_embedding():

        return (
            np.random.rand(128)
            .tolist()
        )