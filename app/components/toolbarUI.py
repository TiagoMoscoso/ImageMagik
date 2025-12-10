import os
import math
import re
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
        self.docs = []
        self.current_index = None


    def load_raw_with_meta(self, raw_path: str) -> np.ndarray:
        with open(raw_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            raise ValueError("Arquivo RAW está vazio.")

        tokens = re.split(r"\s+", content)

        try:
            values = np.array([int(t) for t in tokens], dtype=np.uint8)
        except ValueError as e:
            raise ValueError(f"RAW contém valores não numéricos ou inválidos: {e}")

        num_pixels = values.size
        dim = int(math.isqrt(num_pixels))

        if dim * dim != num_pixels:
            raise ValueError(
                f"Erro: o arquivo RAW tem {num_pixels} valores, "
                f"não forma um quadrado perfeito (dim^2 = {dim * dim})."
            )

        width = dim
        height = dim

        return values.reshape((height, width))


    def on_add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Adicionar imagens RAW",
            os.getcwd(),
            "Imagens (*.raw)"
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
            self,
            "Exportar imagem",
            "saida.raw",
            "RAW (*.raw);;"
        )
        if not path:
            return

        try:
            img = doc.current

            # garante que é uint8 e 2D (escala de cinza)
            if img.ndim == 3:
                # se for RGB/RGBA, converte usando o mesmo pipeline do PIL
                pil_img = numpy_to_pil(img).convert("L")
                pixels = list(pil_img.getdata())
            else:
                # assume já ser escala de cinza
                arr = img.astype(np.uint8).flatten()
                pixels = arr.tolist()

            # salva RAW em TEXTO: "0 34 255 18 ..."
            with open(path, "w", encoding="utf-8") as f_raw:
                f_raw.write(" ".join(str(int(v)) for v in pixels))

            QMessageBox.information(self, "OK", f"Imagem RAW (texto) exportada em:\n{path}")

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao salvar: {e}")

