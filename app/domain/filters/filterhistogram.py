import numpy as np
from app.domain.filter import Filter


class Filter_histogram(Filter):
    def apply(self, img: np.ndarray, **kwargs) -> np.ndarray:
        # garante grayscale
        gray = self.ensure_gray(img)
        
        # calcula histograma
        hist, _ = np.histogram(gray.flatten(), bins=256, range=(0, 255))

        # tamanho da imagem do histograma
        hist_width = 256
        hist_height = 128

        # imagem branca para desenhar o histograma
        hist_img = np.full((hist_height, hist_width), 255, dtype=np.uint8)

        # normaliza o histograma para caber na altura
        max_val = np.max(hist)
        if max_val == 0:
            return hist_img  # evita divisao por zero

        scaled = (hist / max_val) * (hist_height - 1)

        # desenha o histograma (barras verticais pretas)
        for x in range(256):
            h = int(scaled[x])
            hist_img[hist_height - 1 - h : hist_height, x] = 0

        return hist_img
