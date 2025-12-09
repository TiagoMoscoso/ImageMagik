import numpy as np
from app.domain.filter import Filter


class Filter_threshold(Filter):
    def apply(self, img: np.ndarray, threshold: int = 128, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        height, width = gray.shape
        output = np.zeros((height, width), dtype=np.uint8)

        # mantem threshold dentro de 0 a 255
        threshold = max(0, min(threshold, 255))

        for y in range(height):     # linha
            for x in range(width):  # coluna
                value = int(gray[y, x])

                # aplica limiarizacao
                output[y, x] = 255 if value >= threshold else 0

        return output
