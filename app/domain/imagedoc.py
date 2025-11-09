import numpy as np


class ImageDoc:
    def __init__(self, path: str, arr: np.ndarray):
        self.path = path
        self.original = arr.copy()  # RGBA ou L
        self.current = arr.copy()