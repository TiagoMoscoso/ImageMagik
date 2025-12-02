import numpy as np
from app.domain.filter import Filter


class Filter_mask(Filter):
    def apply(self, img: np.ndarray, mask: np.ndarray, **kwargs) -> np.ndarray:
        base = self.ensure_gray(img)
        m = self.ensure_gray(mask)

        h = min(base.shape[0], m.shape[0])
        w = min(base.shape[1], m.shape[1])

        base_c = base[:h, :w].astype(np.uint16)
        mask_c = m[:h, :w].astype(np.uint16)

        out = (base_c * mask_c) // 255
        return out.astype(np.uint8)