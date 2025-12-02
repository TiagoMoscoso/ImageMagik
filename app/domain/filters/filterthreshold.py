import numpy as np
from app.domain.filter import Filter


class Filter_threshold(Filter):
    def apply(self, img: np.ndarray, threshold: int = 128, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        h, w = gray.shape
        out = np.zeros((h, w), dtype=np.uint8)

        if threshold < 0:
            threshold = 0
        elif threshold > 255:
            threshold = 255

        for i in range(h):
            for j in range(w):
                v = int(gray[i, j])
                out[i, j] = 255 if v >= threshold else 0

        return out
