import numpy as np
from app.domain.filter import Filter


class Filter_brightness(Filter):
    def apply(self, img: np.ndarray, factor: float = 1.2, **kwargs) -> np.ndarray:
        rgb = self.as_rgb(img).astype(np.float32)
        out = np.clip(rgb * factor, 0, 255)
        return self.rejoin_rgba(out.astype(np.uint8), img)
