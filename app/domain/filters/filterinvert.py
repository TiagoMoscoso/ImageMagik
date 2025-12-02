import numpy as np
from app.domain.filter import Filter


class Filter_invert(Filter):
    def apply(self, img: np.ndarray, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        h, w = gray.shape
        out = np.zeros((h, w), dtype=np.uint8)

        for i in range(h):
            for j in range(w):
                v = int(gray[i, j])
                out[i, j] = 255 - v

        return out
