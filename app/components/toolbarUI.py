
import os
from PIL import Image

from app.domain.imageconverter import numpy_to_pil, pil_to_numpy
from PySide6.QtWidgets import (
    QListWidgetItem, QFileDialog, QFormLayout, QMessageBox
)
from PySide6.QtGui import QPixmap

class ToolbarUI:
    def __init__(self):
        self.params_form = QFormLayout() 
        
    def on_add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Adicionar imagens",
            os.getcwd(),
            "Imagens (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        for f in files:
            try:
                arr = pil_to_numpy(Image.open(f))
                doc = self.ImageDoc(f, arr)
                self.docs.append(doc)
                item = QListWidgetItem(os.path.basename(f))
                item.setToolTip(f)
                self.listw.addItem(item)
                if self.current_index is None:
                    self.listw.setCurrentRow(0)
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Falha ao abrir {f}\n{e}")

    def on_remove_selected(self):
        idx = self.listw.currentRow()
        if idx < 0:
            return
        self.docs.pop(idx)
        self.listw.takeItem(idx)
        if self.docs:
            self.listw.setCurrentRow(min(idx, len(self.docs) - 1))
        else:
            self.current_index = None
            self.image_label.setText("Abra uma imagem…")
            self.image_label.setPixmap(QPixmap())

    def on_export_image(self):
        doc = self.get_current_doc()
        if not doc:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar imagem", "saida.png",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tif *.tiff)"
        )
        if not path:
            return
        try:
            numpy_to_pil(doc.current).save(path)
            QMessageBox.information(self, "OK", f"Imagem exportada em:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao salvar: {e}")