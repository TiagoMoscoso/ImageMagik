import numpy as np
from app.domain.filter import Filter


class Filter_kernel(Filter):
    def apply(self, img: np.ndarray, kernel: np.ndarray = None, **kwargs) -> np.ndarray:

        # aplica convolucao generica
        result = self.convolve(img, kernel)

        return result
