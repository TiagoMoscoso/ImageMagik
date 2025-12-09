import numpy as np
from app.domain.filter import Filter


class Filter_contrast(Filter):
    def apply(self, img: np.ndarray, factor: float = 1.2, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        height, width = gray.shape
        output = np.zeros((height, width), dtype=np.uint8)

        # percorre cada pixel
        for y in range(height):     # linha
            for x in range(width):  # coluna
                value = int(gray[y, x])

                # aplica contraste: desloca do meio (128), multiplica e volta
                new_value = int((value - 128) * factor + 128)

                # clamping para manter dentro de 0 a 255
                new_value = max(0, min(new_value, 255))

                output[y, x] = new_value

        return output
