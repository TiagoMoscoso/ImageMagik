from app.domain.imageconverter import qimage_from_numpy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from app.domain.imagedoc import ImageDoc


class SelectionUI:
        
    def on_select_index(self, row: int):
            self.current_index = row if 0 <= row < len(self.docs) else None
            self.update_preview()

    def update_preview(self):
        doc = self.get_current_doc()
        if not doc:
            return
        qimg = qimage_from_numpy(doc.current)
        pix = QPixmap.fromImage(qimg)
        target = self.image_label.size()
        self.image_label.setPixmap(pix.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.update_preview()

    def get_current_doc(self) -> ImageDoc | None:
        if self.current_index is None:
            return None
        if 0 <= self.current_index < len(self.docs):
            return self.docs[self.current_index]
        return None