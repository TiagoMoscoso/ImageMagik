import numpy as np
from app.domain.filter import Filter


class Filter_grayscale(Filter):
    def apply(self,img: np.ndarray, **kwargs) -> np.ndarray:
        if img.ndim == 2:
            return img
        rgb = self.as_rgb(img).astype(np.float32)
        gray = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2])
        gray = np.clip(gray, 0, 255).astype(np.uint8)
        return gray