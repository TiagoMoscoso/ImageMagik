import numpy as np
from app.domain.filter import Filter


class Filter_kernel:
    def apply(self,img: np.ndarray, kernel: np.ndarray = None, **kwargs) -> np.ndarray:
        if kernel is None:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)  # sharpen
        rgb = self.as_rgb(img)
        out = np.zeros_like(rgb)
        for c in range(3):
            out[..., c] = self.convolve_channel(rgb[..., c], kernel)
        return self.rejoin_rgba(out, img)