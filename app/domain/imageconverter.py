import numpy as np
from PIL import Image
from PySide6.QtGui import QImage
from typing import Any, Dict, List
# -------------------- Util: conversões QImage <-> NumPy -------------------- #
def qimage_from_numpy(arr: np.ndarray) -> QImage:
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    if arr.ndim == 2:
        h, w = arr.shape
        fmt = QImage.Format_Grayscale8
        qimg = QImage(arr.data, w, h, w, fmt)
        return qimg.copy()
    elif arr.ndim == 3 and arr.shape[2] in (3, 4):
        h, w, c = arr.shape
        if c == 3:
            # Convert RGB -> RGBA
            rgba = np.concatenate([arr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=2)
        else:
            rgba = arr
        qimg = QImage(rgba.data, w, h, w*4, QImage.Format_RGBA8888)
        return qimg.copy()
    else:
        raise ValueError("Array com formato inválido para QImage.")

def numpy_from_qimage(qimg: QImage) -> np.ndarray:
    qimg = qimg.convertToFormat(QImage.Format_RGBA8888)
    w, h = qimg.width(), qimg.height()
    ptr = qimg.constBits()
    arr = np.array(ptr).reshape(h, w, 4)
    return arr

def pil_to_numpy(img: Image.Image) -> np.ndarray:
    if img.mode not in ("RGB", "RGBA", "L"):
        img = img.convert("RGBA")
    arr = np.array(img)
    if arr.ndim == 2:
        return arr
    if arr.shape[2] == 3:
        # pad alpha
        h, w, _ = arr.shape
        alpha = np.full((h, w, 1), 255, dtype=np.uint8)
        arr = np.concatenate([arr, alpha], axis=2)
    return arr

def numpy_to_pil(arr: np.ndarray) -> Image.Image:
    if arr.ndim == 2:
        return Image.fromarray(arr, mode="L")
    if arr.shape[2] == 4:
        return Image.fromarray(arr, mode="RGBA")
    if arr.shape[2] == 3:
        return Image.fromarray(arr, mode="RGB")
    raise ValueError("Formato inválido para PIL.")

def parse_kernel(params: Dict[str, Any]) -> np.ndarray:
    rows = int(params.get("rows", 3))
    cols = int(params.get("cols", 3))
    raw = str(params.get("weights", "")).strip()
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    vals: List[float] = []
    for ln in lines:
        vals.extend([float(x) for x in ln.replace(",", " ").split()])
    arr = np.array(vals, dtype=np.float32)
    if arr.size != rows * cols:
        raise ValueError("Quantidade de pesos não bate com rows*cols.")
    return arr.reshape(rows, cols)