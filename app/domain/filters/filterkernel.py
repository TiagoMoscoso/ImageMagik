import numpy as np
from app.domain.filter import Filter


class Filter_kernel(Filter):
    def apply(self, img: np.ndarray, kernel: np.ndarray = None, **kwargs) -> np.ndarray:
        if kernel is None:
            kernel = np.array(
                [[0, -1, 0],
                 [-1, 5, -1],
                 [0, -1, 0]],
                dtype=float
            )

        return self.convolve(img, kernel)
