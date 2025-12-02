import os
import numpy as np

from PySide6.QtWidgets import (
    QListWidgetItem,
    QFileDialog,
    QFormLayout,
    QMessageBox
)
from PySide6.QtGui import QPixmap

from app.domain.imageconverter import numpy_to_pil
from app.domain.imagedoc import ImageDoc


class ToolbarUI:
    def __init__(self):
        self.params_form = QFormLayout()


    def load_raw_with_meta(self, raw_path: str) -> np.ndarray:
        """
        Lê um arquivo .raw (8 bits/pixel, grayscale) usando um arquivo
        de metadados '<nome>_meta.txt' no formato:

            <largura> <altura>
        """
        base, _ = os.path.splitext(raw_path)
        meta_path = base + "_meta.txt"

        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadados não encontrados: {meta_path}")

        with open(meta_path, "r", encoding="utf-8") as f:
            parts = f.read().strip().split()
            if len(parts) < 2:
                raise ValueError(
                    f"Meta inválido em {meta_path}. "
                    f"Esperado: 'largura altura'."
                )
            width, height = map(int, parts[:2])

        data = np.fromfile(raw_path, dtype=np.uint8)
        expected_size = width * height

        if data.size != expected_size:
            raise ValueError(
                f"Tamanho do RAW ({data.size}) não bate com "
                f"largura x altura ({expected_size})."
            )

        return data.reshape((height, width))


    def on_add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Adicionar imagens RAW",
            os.getcwd(),
<<<<<<< HEAD
            "Imagens (*.raw)"
=======
            "Imagens RAW (*.raw)"
>>>>>>> 57863f5 (.raw alteracao)
        )

        for f in files:
            try:
                arr = self.load_raw_with_meta(f)
                doc = ImageDoc(f, arr) 
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
            self.image_label.setText("Abra uma imagem RAW…")
            self.image_label.setPixmap(QPixmap())

    def on_export_image(self):
        doc = self.get_current_doc()
        if not doc:
            return

        path, _ = QFileDialog.getSaveFileName(
<<<<<<< HEAD
            self, "Exportar imagem", "saida.png",
            "RAW (*.raw);;"
=======
            self,
            "Exportar imagem",
            "saida.png",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tif *.tiff)"
>>>>>>> 57863f5 (.raw alteracao)
        )
        if not path:
            return

        try:
            numpy_to_pil(doc.current).save(path)
            QMessageBox.information(self, "OK", f"Imagem exportada em:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao salvar: {e}")
