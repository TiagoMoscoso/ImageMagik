import numpy as np
from app.domain.filter import Filter


class Filter_invert(Filter):
    def apply(self,img: np.ndarray, **kwargs) -> np.ndarray:
        rgb = self.as_rgb(img).astype(np.int16)
        out = 255 - rgb
        return self.rejoin_rgba(out.astype(np.uint8), img)
