import numpy as np
from app.domain.filter import Filter


class Filter_contrast(Filter):
    def apply(self, img: np.ndarray, factor: float = 1.2, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        h, w = gray.shape
        out = np.zeros((h, w), dtype=np.uint8)

        for i in range(h):
            for j in range(w):
                v = int(gray[i, j])
                v = int((v - 128) * factor + 128)
                if v < 0:
                    v = 0
                elif v > 255:
                    v = 255
                out[i, j] = v

        return out
