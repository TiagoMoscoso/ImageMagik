import numpy as np
from app.domain.filter import Filter


class Filter_difference(Filter):
    def apply(self, img: np.ndarray, other: np.ndarray, **kwargs) -> np.ndarray:
        # garante que as duas imagens estao em escala de cinza
        base = self.ensure_gray(img)
        other_gray = self.ensure_gray(other)

        # calcula dimensoes validas
        height = min(base.shape[0], other_gray.shape[0])
        width = min(base.shape[1], other_gray.shape[1])

        # recorta as duas imagens para o mesmo tamanho
        base_cut = base[:height, :width].astype(np.int16)
        other_cut = other_gray[:height, :width].astype(np.int16)

        # diferença absoluta
        diff = np.abs(base_cut - other_cut)

        # clamping para 0–255
        diff = np.clip(diff, 0, 255).astype(np.uint8)

        return diff
