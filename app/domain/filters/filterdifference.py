import numpy as np
from app.domain.filter import Filter

class Filter_difference(Filter):
    def apply(self, img: np.ndarray, other: np.ndarray, **kwargs) -> np.ndarray:
        # garante que as duas imagens estão em escala de cinza
        base = self.ensure_gray(img)
        other_gray = self.ensure_gray(other)

        # calcula dimensões válidas
        height = min(base.shape[0], other_gray.shape[0])
        width = min(base.shape[1], other_gray.shape[1])

        # cria imagem de saída manualmente
        diff_img = np.zeros((height, width), dtype=np.uint8)

        # calculo manual da diferença absoluta pixel a pixel
        for i in range(height):
            for j in range(width):

                # lê os pixels e converte pra int
                a = int(base[i, j])
                b = int(other_gray[i, j])

                # diferença absoluta manual
                d = a - b
                if d < 0:
                    d = -d

                # clamp manual para 0–255
                if d < 0:
                    d = 0
                elif d > 255:
                    d = 255

                diff_img[i, j] = d

        return diff_img
