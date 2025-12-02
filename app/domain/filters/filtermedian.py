import numpy as np
from app.domain.filter import Filter


class Filter_median(Filter):
    def apply(self, img: np.ndarray, size: int = 3, **kwargs) -> np.ndarray:
        gray = self.ensure_gray(img)
        h, w = gray.shape
        out = np.zeros((h, w), dtype=np.uint8)

        if size < 1:
            size = 1
        if size % 2 == 0:
            size += 1

        r = size // 2

        for i in range(h):
            for j in range(w):
                valores: list[int] = []

                for di in range(-r, r + 1):
                    ii = i + di
                    if ii < 0:
                        ii = 0
                    elif ii >= h:
                        ii = h - 1

                    for dj in range(-r, r + 1):
                        jj = j + dj
                        if jj < 0:
                            jj = 0
                        elif jj >= w:
                            jj = w - 1

                        valores.append(int(gray[ii, jj]))

                valores.sort()
                mid = len(valores) // 2
                out[i, j] = valores[mid]

        return out
