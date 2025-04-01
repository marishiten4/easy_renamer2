from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QSplitter
from PyQt5.QtGui import QPalette, QColor, QIcon
from ui.image_list import ImageList
from ui.preview import Preview
from ui.word_blocks import WordBlocks
from ui.settings_dialog import SettingsDialog
from core.renamer import Renamer
from utils.helpers import count_fullwidth_chars
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Easy Renamer")
        self.resize(1000, 700)
        if os.path.exists("assets/icon.ico"):
            self.setWindowIcon(QIcon("assets/icon.ico"))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        splitter = QSplitter()
        self.main_layout.addWidget(splitter)
        
        self.image_list = ImageList()
        splitter.addWidget(self.image_list)
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.preview = Preview()
        self.word_blocks = WordBlocks()
        self.warning_label = QLabel("")
        self.folder_button = QPushButton("フォルダ選択")
        self.settings_button = QPushButton("設定")
        self.rename_button = QPushButton("リネーム実行")
        
        # アイコンをボタンに設定
        if os.path.exists("assets/icon.ico"):
            self.folder_button.setIcon(QIcon("assets/icon.ico"))
            self.settings_button.setIcon(QIcon("assets/icon.ico"))
            self.rename_button.setIcon(QIcon("assets/icon.ico"))
        
        right_layout.addWidget(QLabel("プレビュー:"))
        right_layout.addWidget(self.preview, 2)
        right_layout.addWidget(self.word_blocks, 1)
        right_layout.addWidget(self.warning_label)
        right_layout.addWidget(self.folder_button)
        right_layout.addWidget(self.settings_button)
        right_layout.addWidget(self.rename_button)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 700])
        
        self.folder_button.clicked.connect(self.select_folder)
        self.rename_button.clicked.connect(self.execute_rename)
        self.settings_button.clicked.connect(self.open_settings)
        self.image_list.itemClicked.connect(self.update_preview)
        self.word_blocks.pattern_input.textChanged.connect(self.check_pattern)
        
        self.renamer = Renamer()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            self.image_list.load_images(folder)
    
    def update_preview(self, item):
        image_path = item.data(32)
        self.preview.update_image(image_path)
        metadata = self.renamer.get_metadata(image_path)
        self.word_blocks.update_candidates(metadata)
    
    def check_pattern(self):
        pattern = self.word_blocks.get_rename_pattern()
        char_count = count_fullwidth_chars(pattern)
        if char_count > 65:
            self.warning_label.setText("警告: 文字数が65文字を超えています")
            self.warning_label.setStyleSheet("color: red;")
        else:
            self.warning_label.clear()
    
    def execute_rename(self):
        selected_images = self.image_list.selected_images()
        self.renamer.rename_files(selected_images, self.word_blocks.get_rename_pattern(), self)
    
    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()
