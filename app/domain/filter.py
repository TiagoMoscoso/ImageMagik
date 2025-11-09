import numpy as np

class Filter:

    def as_rgb(self, arr: np.ndarray) -> np.ndarray:
        if arr.ndim == 2:
            return np.stack([arr, arr, arr], axis=2)
        if arr.shape[2] == 4:
            return arr[..., :3]
        return arr

    def rejoin_rgba(self, rgb: np.ndarray, base: np.ndarray) -> np.ndarray:
        if base.ndim == 2:
            return rgb[..., 0]
        if base.shape[2] == 4:
            a = base[..., 3:4]
            return np.concatenate([rgb, a], axis=2)
        return rgb
    
    def convolve_channel(self, ch: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        kh, kw = kernel.shape
        pad_h, pad_w = kh // 2, kw // 2
        padded = np.pad(ch, ((pad_h, pad_h), (pad_w, pad_w)), mode="reflect")
        out = np.zeros_like(ch, dtype=np.float32)
        for i in range(ch.shape[0]):
            roi = padded[i:i+kh, :]
            for j in range(ch.shape[1]):
                patch = roi[:, j:j+kw]
                out[i, j] = np.sum(patch * kernel)
        return np.clip(out, 0, 255).astype(np.uint8)
