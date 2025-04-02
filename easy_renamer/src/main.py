import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists("assets/icon.ico"):
        app.setWindowIcon(QIcon("assets/icon.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
