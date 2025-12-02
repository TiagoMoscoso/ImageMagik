import numpy as np
from app.domain.filter import Filter


class Filter_laplacian(Filter):
    def apply(self, img: np.ndarray, **kwargs) -> np.ndarray:
        kernel = np.array(
            [[0, -1,  0],
             [-1, 4, -1],
             [0, -1,  0]],
            dtype=float
        )
        out = self.convolve(img, kernel)
        return out
