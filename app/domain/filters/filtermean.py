import numpy as np
from app.domain.filter import Filter


class Filter_mean(Filter):
    def apply(self, img: np.ndarray, size: int = 3, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        h, w = gray.shape

        # ajusta tamanho da mascara
        if size < 1:
            size = 1
        if size % 2 == 0:
            size += 1  # forca ser sempre impar

        r = size // 2  # raio da mascara

        out = np.zeros((h, w), dtype=np.uint8)

        for i in range(h): # linha
            for j in range(w): # coluna

                acc = 0     # soma dos valores da vizinhança
                count = 0   # numero de pixels considerados

                #percorre a vizinhança
                for di in range(-r, r + 1):
                    for dj in range(-r, r + 1):

                        #cordenadas da vizinhança
                        ii = i + di
                        jj = j + dj

                        #clamping replicacao da borda
                        ii = min(max(ii, 0), h - 1)
                        jj = min(max(jj, 0), w - 1)

                        acc += int(gray[ii, jj])
                        count += 1

                # media
                out[i, j] = acc // count

        return out
