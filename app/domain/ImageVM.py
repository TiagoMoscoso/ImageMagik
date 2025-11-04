from __future__ import annotations
import os, tempfile, time
from typing import Dict, Any
from PIL import Image, ImageOps
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from .filters import FILTERS, FILTERS_LIST


class ImageVM(QObject):
    activeModeChanged = Signal()
    imageChanged = Signal()
    selectionChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._activeMode = "color"
        self._image: Image.Image | None = None
        self._imageWidth = 0
        self._imageHeight = 0
        self._colorUrl = ""
        self._grayUrl = ""
        self._x0 = self._y0 = self._x1 = self._y1 = 0

    def getActiveMode(self) -> str:
        return self._activeMode

    @Slot(str)
    def setActive(self, mode: str) -> None:
        if mode in ("color", "gray") and self._activeMode != mode:
            self._activeMode = mode
            self.activeModeChanged.emit()

    activeMode = Property(str, fget=getActiveMode, notify=activeModeChanged)

    colorUrl = Property(str, fget=lambda s: s._colorUrl, notify=imageChanged)
    grayUrl  = Property(str, fget=lambda s: s._grayUrl,  notify=imageChanged)
    imageWidth  = Property(int, fget=lambda s: s._imageWidth,  notify=imageChanged)
    imageHeight = Property(int, fget=lambda s: s._imageHeight, notify=imageChanged)

    @Property("QVariant", constant=True)
    def filters(self):
        return FILTERS_LIST

    @Slot(str)
    def openImage(self, qurl: str) -> None:
        path = QUrl(qurl).toLocalFile() if qurl.startswith("file:") else qurl
        img = Image.open(path).convert("RGBA")
        self._image = img
        self._imageWidth, self._imageHeight = img.size
        self._colorUrl = self._save_temp(img)
        self._grayUrl  = self._save_temp(ImageOps.grayscale(img).convert("RGBA"))
        self.imageChanged.emit()

    @Slot(int, int, int, int)
    def updateSelection(self, x0: int, y0: int, x1: int, y1: int) -> None:
        self._x0, self._y0, self._x1, self._y1 = x0, y0, x1, y1
        self.selectionChanged.emit()

    @Slot(str, "QVariant")
    def applyFilter(self, key: str, args) -> None:
        if self._image is None or key not in FILTERS:
            return
        filt = FILTERS[key]
        coords = (self._x0, self._y0, self._x1, self._y1)
        py_args: Dict[str, Any] = dict(args) if isinstance(args, dict) else {}
        out = filt.apply(self._image, coords, py_args)

        self._image = out
        self._imageWidth, self._imageHeight = out.size
        self._colorUrl = self._save_temp(out)
        self._grayUrl  = self._save_temp(ImageOps.grayscale(out).convert("RGBA"))
        self.imageChanged.emit()

    def _save_temp(self, pil_img: Image.Image) -> str:
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        pil_img.save(path, "PNG")
        url = QUrl.fromLocalFile(path).toString()
        return f"{url}?t={int(time.time()*1000)}"
