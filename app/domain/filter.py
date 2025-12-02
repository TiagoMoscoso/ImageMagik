import numpy as np

class Filter:
    def ensure_gray(self, img: np.ndarray) -> np.ndarray:
        arr = np.asarray(img)

        if arr.ndim != 2:
            raise ValueError(f"Imagem inválida para RAW: esperado 2D, veio shape={arr.shape}")
        
        if arr.dtype != np.uint8:
            arr = arr.astype(np.uint8)

        return arr

    def convolve(self, img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        gray = self.ensure_gray(img)
        h, w = gray.shape

        k = np.asarray(kernel, dtype=float)
        kh, kw = k.shape
        pad_h = kh // 2
        pad_w = kw // 2

        out = np.zeros((h, w), dtype=float)

        for i in range(h):
            for j in range(w):
                acc = 0.0
                # percorre a mascara
                for ki in range(kh):
                    for kj in range(kw):
                        ii = i + ki - pad_h
                        jj = j + kj - pad_w

                        # trata borda
                        if ii < 0:
                            ii = 0
                        elif ii >= h:
                            ii = h - 1

                        if jj < 0:
                            jj = 0
                        elif jj >= w:
                            jj = w - 1

                        acc += float(gray[ii, jj]) * k[ki, kj]

                out[i, j] = acc

        out = np.clip(out, 0, 255)
        return out.astype(np.uint8)
