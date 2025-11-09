import os
from typing import List
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QPixmap, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QFileDialog, QLabel, QToolBar,
    QComboBox, QFormLayout,QPushButton, QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtGui import QPalette, QGuiApplication
from PIL import Image
from app.components.applyUI import ApplyUI
from app.components.parametersUI import ParametersUI
from app.components.selectionUI import SelectionUI
from app.components.toolbarUI import ToolbarUI
from app.domain.filterslist import FILTERS
from app.domain.imageconverter import numpy_to_pil, pil_to_numpy
from app.domain.imagedoc import ImageDoc

class MainWindow(QMainWindow, ParametersUI, ToolbarUI, SelectionUI, ApplyUI):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Magik")
        self.setWindowIcon(QIcon("assets/tuxmage.png"))
        self.resize(1200, 720)

        self.docs: List[ImageDoc] = []
        self.current_index: int | None = None

        tb = QToolBar("Main", self)
        tb.setIconSize(QSize(18, 18))
        self.addToolBar(Qt.TopToolBarArea, tb)

        act_add = QAction("Adicionar", self)
        act_add.setShortcut("Ctrl+O")
        act_add.triggered.connect(self.on_add_images)
        tb.addAction(act_add)

        act_remove = QAction("Remover", self)
        act_remove.setShortcut("Del")
        act_remove.triggered.connect(self.on_remove_selected)
        tb.addAction(act_remove)

        act_save = QAction("Exportar", self)
        act_save.setShortcut("Ctrl+S")
        act_save.triggered.connect(self.on_export_image)
        tb.addAction(act_save)


        root = QWidget()
        self.setCentralWidget(root)
        h = QHBoxLayout(root)
        h.setContentsMargins(8, 8, 8, 8)
        h.setSpacing(8)

        self.listw = QListWidget()
        self.listw.currentRowChanged.connect(self.on_select_index)
        self.listw.setMinimumWidth(240)
        h.addWidget(self.listw, 0)

        center_wrap = QFrame()
        center_wrap.setFrameShape(QFrame.StyledPanel)
        v_center = QVBoxLayout(center_wrap)
        v_center.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel("Abra uma imagem…")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setBackgroundRole(QPalette.Base if hasattr(QPalette, 'Base') else None)
        v_center.addWidget(self.image_label, 1)
        h.addWidget(center_wrap, 1)

        self.right = QFrame()
        self.right.setFrameShape(QFrame.StyledPanel)
        vr = QVBoxLayout(self.right)
        vr.setSpacing(6)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(FILTERS.keys())
        self.filter_combo.currentTextChanged.connect(self.rebuild_params_form)
        vr.addWidget(self.filter_combo)

        self.params_form = QFormLayout()
        vr.addLayout(self.params_form)

        self.btn_apply = QPushButton("Aplicar")
        self.btn_apply.clicked.connect(self.on_apply_filter)
        vr.addWidget(self.btn_apply)

        vr.addStretch(1)
        h.addWidget(self.right, 0)
        
        self.FILTER_PANEL_RATIO = 0.2
        screen_w = QGuiApplication.primaryScreen().availableGeometry().width()
        target_w = int(screen_w * self.FILTER_PANEL_RATIO)
        self.right.setFixedWidth(target_w)
        self.right.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.rebuild_params_form(self.filter_combo.currentText())

    def on_add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Adicionar imagens",
            os.getcwd(),
            "Imagens (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        for f in files:
            try:
                arr = pil_to_numpy(Image.open(f))
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