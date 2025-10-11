import sys, tempfile
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from pathlib import Path
from PIL import Image

TMP_DIR = Path(tempfile.gettempdir())
COLOR_PREVIEW = TMP_DIR / "qml_edit_color.png"
GRAY_PREVIEW  = TMP_DIR / "qml_edit_gray.png"


class ImageVM(QObject):
    # signals
    colorUrlChanged = Signal(QUrl)
    grayUrlChanged  = Signal(QUrl)
    activeModeChanged = Signal(str)
    coordsChanged = Signal(int, int, int, int)
    sizeChanged = Signal(int, int)

    def __init__(self):
        super().__init__()
        self._src_path: Path | None = None
        self._color_url = QUrl()
        self._gray_url  = QUrl()
        self._active_mode = "color"  # "color" | "gray"
        self._iw = 0
        self._ih = 0

    # ---- properties expostas ao QML ----
    def getColorUrl(self) -> QUrl:
        return self._color_url
    colorUrl = Property(QUrl, fget=getColorUrl, notify=colorUrlChanged)

    def getGrayUrl(self) -> QUrl:
        return self._gray_url
    grayUrl = Property(QUrl, fget=getGrayUrl, notify=grayUrlChanged)

    def getActiveMode(self) -> str:
        return self._active_mode
    def setActiveMode(self, mode: str):
        if mode not in ("color", "gray"):
            return
        if mode != self._active_mode:
            self._active_mode = mode
            self.activeModeChanged.emit(self._active_mode)
    activeMode = Property(str, fget=getActiveMode, fset=setActiveMode, notify=activeModeChanged)

    def getImageWidth(self) -> int:
        return self._iw
    def getImageHeight(self) -> int:
        return self._ih
    imageWidth  = Property(int, fget=getImageWidth, notify=sizeChanged)
    imageHeight = Property(int, fget=getImageHeight, notify=sizeChanged)

    # ---- slots chamados pelo QML ----
    @Slot(str)
    def openImage(self, file_url: str):
        url = QUrl(file_url)
        path = Path(url.toLocalFile()) if url.isLocalFile() else Path(file_url)
        if not path.exists():
            return
        self._src_path = path
        self._process_pipeline()

    @Slot(str)
    def setActive(self, mode: str):
        self.setActiveMode(mode)

    @Slot(int, int, int, int)
    def updateSelection(self, x0: int, y0: int, x1: int, y1: int):
        # Coordenadas sempre no espaço da imagem (pixels reais)
        self.coordsChanged.emit(x0, y0, x1, y1)

    # ---- processamento ----
    def _process_pipeline(self):
        try:
            img = Image.open(self._src_path)

            # 1) Normaliza para edição (RGB/RGBA)
            edit_img = self.normalize_for_editing(img)

            # Guarda dimensões reais da imagem processada
            self._iw, self._ih = edit_img.size
            self.sizeChanged.emit(self._iw, self._ih)

            # 2) Gera versão em tons de cinza
            gray_img = edit_img.convert("L")

            # 3) Salva prévias (PNG sem perder nitidez)
            edit_img.save(COLOR_PREVIEW)
            gray_img.save(GRAY_PREVIEW)

            # 4) Atualiza URLs no QML
            self._color_url = QUrl.fromLocalFile(str(COLOR_PREVIEW))
            self._gray_url  = QUrl.fromLocalFile(str(GRAY_PREVIEW))
            self.colorUrlChanged.emit(self._color_url)
            self.grayUrlChanged.emit(self._gray_url)

            # Reseta modo ativo para “color” (padrão)
            self.setActiveMode("color")

        except Exception as e:
            print("Processing error:", e, file=sys.stderr)
            
    def normalize_for_editing(self, img: Image.Image) -> Image.Image:
        """
        Normaliza a imagem para um formato padrão de edição:
        - Mantém alpha se existir: RGBA
        - Caso contrário: RGB
        - Converte paleta/CMYK/YCbCr/LAB/HSV/I/F para RGB/RGBA
        """
        m = img.mode
        if m in ("LA", "RGBA"):
            return img.convert("RGBA")
        if m == "RGB":
            return img
        if m == "L":
            return img.convert("RGB")
        return img.convert("RGB")
