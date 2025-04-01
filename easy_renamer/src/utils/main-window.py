import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFileDialog, QTabWidget, QMessageBox,
    QListWidget, QListWidgetItem, QFrame, QRadioButton, QButtonGroup,
    QScrollArea, QComboBox, QSpinBox, QProgressBar, QSplitter,
    QTextEdit, QDialog, QGroupBox, QGridLayout, QApplication
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPixmap

from src.core.renamer import EasyRenamer
from src.ui.image_list import ImageListWidget
from src.ui.preview import ImagePreviewWidget
from src.ui.word_blocks import WordBlocksWidget
from src.ui.settings_dialog import SettingsDialog
from src.utils.helpers import get_resource_path, count_characters, create_zip