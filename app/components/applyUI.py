from PySide6.QtWidgets import QMessageBox
from app.domain.filterslist import FILTERS, parse_kernel

class ApplyUI:
    def on_apply_filter(self):
        doc = self.get_current_doc()
        if not doc:
            return
        fname = self.filter_combo.currentText()
        spec = FILTERS[fname]
        params = self.read_params()
        try:
            if spec is FILTERS["Custom Kernel"]:
                kernel = parse_kernel(params)
                new = spec.func(doc.current, kernel=kernel)
            else:
                new = spec.func(doc.current, **params)
                doc.current = new
                self.update_preview()
        except Exception as e:
            QMessageBox.warning(self, "Erro no filtro", str(e))