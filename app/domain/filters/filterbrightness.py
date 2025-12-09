import numpy as np
from app.domain.filter import Filter


class Filter_brightness(Filter):
    def apply(self, img: np.ndarray, offset: int = 0, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        height, width = gray.shape
        output = np.zeros((height, width), dtype=np.uint8)

        # percorre cada pixel
        for y in range(height):     # linha
            for x in range(width):  # coluna
                value = int(gray[y, x])

                # aplica brilho aditivo
                new_value = value + int(offset)

                # clamping para manter dentro de 0 a 255
                new_value = max(0, min(new_value, 255))

                output[y, x] = new_value

        return output
