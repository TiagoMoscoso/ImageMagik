import sys, os
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from app.domain.ImageVM import ImageVM


def main():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    vm = ImageVM()
    engine.rootContext().setContextProperty("imageVM", vm)
    engine.load(QUrl.fromLocalFile(os.path.abspath("app/components/main.qml")))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
