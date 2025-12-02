import os

from PySide6.QtWidgets import QMessageBox, QListWidgetItem

from app.domain.filterslist import FILTERS
from app.domain.imagedoc import ImageDoc


class ApplyUI:
    def on_apply_filter(self):
        src_doc = self.get_current_doc()
        if not src_doc:
            return

        fname = self.filter_combo.currentText()
        spec = FILTERS[fname]

        params = self.read_params()

        for p in spec.params:
            if p.ptype == "image":
                idx = params.get(p.name, None)
                if idx is None:
                    continue

                if not (0 <= idx < len(self.docs)):
                    QMessageBox.warning(
                        self,
                        "Erro no filtro",
                        f"Índice inválido para parâmetro de imagem '{p.name}': {idx}"
                    )
                    return

                params[p.name] = self.docs[idx].current

        try:
            new_arr = spec.func(src_doc.current, **params)

            base_name = os.path.basename(src_doc.path) if src_doc.path else "imagem"
            display_name = f"{base_name} -> {fname}"

            new_doc = ImageDoc(f"{src_doc.path} | {fname}", new_arr)
            self.docs.append(new_doc)

            item = QListWidgetItem(display_name)
            item.setToolTip(display_name)
            self.listw.addItem(item)
            self.listw.setCurrentRow(self.listw.count() - 1)

        except Exception as e:
            QMessageBox.warning(self, "Erro no filtro", str(e))
