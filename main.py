import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from app.components.mainUI import MainWindow
from qt_material import apply_stylesheet

def main():
    app = QApplication(sys.argv)

    app.setStyle(QStyleFactory.create("Fusion"))

    #apply_stylesheet(app, theme='dark_blue.xml')

    win = MainWindow()
    win.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

