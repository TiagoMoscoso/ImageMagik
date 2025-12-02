from PySide6.QtWidgets import (
    QWidget, QFormLayout, QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit, QComboBox
)
from typing import Dict, Any
import os

from app.domain.filterslist import FILTERS


class ParametersUI:
    def __init__(self):
        self.params_form = QFormLayout() 
        
    def clear_form(self):
        while self.params_form.rowCount():
            self.params_form.removeRow(0)

    def rebuild_params_form(self, name: str):
        self.clear_form()
        spec = FILTERS[name]
        self._param_widgets: Dict[str, QWidget] = {}

        for p in spec.params:
            if p.ptype == "int":
                w = QSpinBox()
                if p.min_val is not None:
                    w.setMinimum(int(p.min_val))
                if p.max_val is not None:
                    w.setMaximum(int(p.max_val))
                w.setValue(int(p.default))
                w.setSingleStep(int(p.step or 1))

            elif p.ptype == "float":
                w = QDoubleSpinBox()
                w.setDecimals(3)
                if p.min_val is not None:
                    w.setMinimum(float(p.min_val))
                if p.max_val is not None:
                    w.setMaximum(float(p.max_val))
                w.setValue(float(p.default))
                w.setSingleStep(float(p.step or 0.1))

            elif p.ptype == "bool":
                w = QCheckBox()
                w.setChecked(bool(p.default))

            elif p.ptype == "text":
                w = QLineEdit()
                w.setText(str(p.default))
                w.setClearButtonEnabled(True)
                w.setMinimumWidth(220)

            elif p.ptype == "image":
                w = QComboBox()
                docs = getattr(self, "docs", [])
                for idx, doc in enumerate(docs):
                    path = getattr(doc, "path", "") or ""
                    label = os.path.basename(path) if path else f"Imagem {idx+1}"
                    w.addItem(label, idx)
                default_idx = int(p.default or 0)
                if 0 <= default_idx < w.count():
                    w.setCurrentIndex(default_idx)

            else:
                continue

            self._param_widgets[p.name] = w
            self.params_form.addRow(p.name, w)

    def read_params(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for name, w in self._param_widgets.items():
            if isinstance(w, QSpinBox):
                out[name] = int(w.value())
            elif isinstance(w, QDoubleSpinBox):
                out[name] = float(w.value())
            elif isinstance(w, QCheckBox):
                out[name] = bool(w.isChecked())
            elif isinstance(w, QLineEdit):
                out[name] = w.text()
            elif isinstance(w, QComboBox):
                data = w.currentData()
                out[name] = int(data) if data is not None else int(w.currentIndex())
        return out
