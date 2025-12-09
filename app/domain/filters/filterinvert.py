import numpy as np
from app.domain.filter import Filter


class Filter_invert(Filter):
    def apply(self, img: np.ndarray, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        height, width = gray.shape
        output = np.zeros((height, width), dtype=np.uint8)

        # percorre cada pixel da imagem
        for y in range(height):     # linha
            for x in range(width):  # coluna
                value = int(gray[y, x])

                # inverte o pixel: 255 - valor_atual
                output[y, x] = 255 - value

        return output
