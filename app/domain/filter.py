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

        # prepara a máscara (kernel)
        k = np.asarray(kernel, dtype=float)
        kh, kw = k.shape

        # metade do tamanho da máscara (offset para bordas)
        pad_h = kh // 2
        pad_w = kw // 2

        # imagem de saída (float para acumular valores)
        out = np.zeros((h, w), dtype=float)

        # percorre cada pixel da imagem
        for i in range(h):
            for j in range(w):

                acc = 0.0  # acumulador da convolução

                # percorre cada elemento da máscara
                for ki in range(kh):
                    for kj in range(kw):

                        # coordenadas do pixel vizinho correspondente à máscara
                        ii = i + ki - pad_h
                        jj = j + kj - pad_w

                        # tratamento de bordas clamping, usa o pixel mais próximo válido
                        if ii < 0:
                            ii = 0
                        elif ii >= h:
                            ii = h - 1

                        if jj < 0:
                            jj = 0
                        elif jj >= w:
                            jj = w - 1

                        # acumula multiplicação pixel * peso do kernel
                        acc += float(gray[ii, jj]) * k[ki, kj]

                # salva o valor acumulado
                out[i, j] = acc

        # clamp final para faixa válida [0, 255] e conversão para 8 bits
        out = np.clip(out, 0, 255)
        return out.astype(np.uint8)

