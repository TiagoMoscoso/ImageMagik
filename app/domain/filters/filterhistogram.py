import numpy as np
from app.domain.filter import Filter


class Filter_histogram(Filter):
    def apply(self, img: np.ndarray, **kwargs) -> np.ndarray:
        # garante grayscale
        gray = self.ensure_gray(img)

        # inicializa histograma manualmente (256 contadores)
        hist = [0] * 256

        # percorre pixel a pixel e contabiliza
        h, w = gray.shape
        for i in range(h):
            for j in range(w):
                val = int(gray[i, j])  # 0..255
                hist[val] += 1

        # tamanho da imagem final do histograma
        hist_width = 256
        hist_height = 128
        hist_img = np.full((hist_height, hist_width), 255, dtype=np.uint8)

        # normaliza manualmente
        max_val = max(hist)
        if max_val == 0:
            return hist_img

        # escala: cada coluna x recebe uma barra proporcional
        for x in range(256):
            scaled_h = int(hist[x] / max_val * (hist_height - 1))
            # desenha de baixo pra cima
            for y in range(hist_height - 1, hist_height - 1 - scaled_h, -1):
                hist_img[y, x] = 0

        return hist_img

