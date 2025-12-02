import numpy as np


class ImageDoc:
    def __init__(self, path: str, arr: np.ndarray):
        self.path = path
        self.original = arr.copy()
        self.current = arr.copy()
