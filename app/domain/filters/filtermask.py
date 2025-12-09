import numpy as np
from app.domain.filter import Filter


class Filter_mask(Filter):
    def apply(self, img: np.ndarray, mask: np.ndarray, **kwargs) -> np.ndarray:
        # garante que ambas as imagens sao grayscale
        base = self.ensure_gray(img)
        mask_gray = self.ensure_gray(mask)

        # calcula largura e altura validas para aplicar o mask
        height = min(base.shape[0], mask_gray.shape[0])
        width = min(base.shape[1], mask_gray.shape[1])

        # recorta para garantir que as duas imagens tenham o mesmo tamanho
        base_cut = base[:height, :width].astype(np.uint16)
        mask_cut = mask_gray[:height, :width].astype(np.uint16)

        # aplica a operacao de multiplicacao normalizada
        # (pixel_base * pixel_mask) / 255
        result = (base_cut * mask_cut) // 255

        return result.astype(np.uint8)
