from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QSplitter, QMessageBox
from PyQt5.QtCore import Qt
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
        self.resize(1400, 900)  # 初期サイズを設定（固定ではない）
        if os.path.exists("assets/icon.ico"):
            self.setWindowIcon(QIcon("assets/icon.ico"))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        self.splitter = QSplitter(Qt.Horizontal)  # インスタンス変数として保持
        self.main_layout.addWidget(self.splitter)
        
        self.image_list = ImageList()
        self.image_list.setMinimumWidth(100)  # 画像一覧の最小幅
        self.splitter.addWidget(self.image_list)
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.preview = Preview()
        self.word_blocks = WordBlocks()
        self.warning_label = QLabel("")
        self.folder_button = QPushButton("フォルダ選択")
        self.refresh_button = QPushButton("再読み込み")
        self.settings_button = QPushButton("設定")
        self.rename_button = QPushButton("リネーム実行")
        
        if os.path.exists("assets/icon.ico"):
            self.folder_button.setIcon(QIcon("assets/icon.ico"))
            self.refresh_button.setIcon(QIcon("assets/icon.ico"))
            self.settings_button.setIcon(QIcon("assets/icon.ico"))
            self.rename_button.setIcon(QIcon("assets/icon.ico"))
        
        right_layout.addWidget(QLabel("プレビュー:"))
        right_layout.addWidget(self.preview, 7)
        right_layout.addWidget(self.word_blocks, 1)
        right_layout.addWidget(self.warning_label)
        right_layout.addWidget(self.folder_button)
        right_layout.addWidget(self.refresh_button)
        right_layout.addWidget(self.settings_button)
        right_layout.addWidget(self.rename_button)
        right_widget.setMinimumWidth(200)  # リネームエリアの最小幅
        
        self.splitter.addWidget(right_widget)
        self.splitter.setSizes([300, 1100])  # 初期サイズ（合計1400px）
        
        # スプリッターのドラッグイベントをハンドリング
        self.splitter.splitterMoved.connect(self.on_splitter_moved)
        self.is_dragging = False
        
        self.folder_button.clicked.connect(self.select_folder)
        self.refresh_button.clicked.connect(self.refresh_metadata)
        self.rename_button.clicked.connect(self.execute_rename)
        self.settings_button.clicked.connect(self.open_settings)
        self.image_list.itemClicked.connect(self.update_preview)
        self.word_blocks.pattern_input.textChanged.connect(self.check_pattern)
        
        self.renamer = Renamer()
        self.current_folder = None  # 選択したフォルダを保持

    def on_splitter_moved(self, pos, index):
        """スプリッターが動いている間のウィンドウサイズ固定"""
        if not self.is_dragging:
            self.is_dragging = True
            self.setFixedSize(self.size())  # ドラッグ開始時にサイズを固定
        # ドラッグ終了を検知するためにタイマーを使用することも可能だが、ここでは簡易的に対応

    def mouseReleaseEvent(self, event):
        """マウスリリースでサイズ固定を解除"""
        if self.is_dragging:
            self.is_dragging = False
            self.setMinimumSize(800, 600)  # 最小サイズを設定
            self.setMaximumSize(16777215, 16777215)  # 最大サイズをデフォルトに戻す（制限解除）

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            self.current_folder = folder
            self.image_list.load_images(folder)
    
    def update_preview(self, item):
        image_path = item.data(32)
        if os.path.exists(image_path):
            self.preview.update_image(image_path)
            metadata = self.renamer.get_metadata(image_path)
            print(f"Translated metadata: {metadata}")
            self.word_blocks.update_candidates(metadata)
        else:
            print(f"Skipping preview update: File not found - {image_path}")
            self.preview.clear()
    
    def refresh_metadata(self):
        self.renamer.update_word_map()
        selected_items = self.image_list.list_widget.selectedItems()
        if selected_items:
            self.update_preview(selected_items[0])
        else:
            print("No selected items to refresh.")
    
    def check_pattern(self):
        pattern = self.word_blocks.get_rename_pattern()
        char_count = count_fullwidth_chars(pattern)
        if char_count > 65:
            self.warning_label.setText("警告: 文字数が65文字を超えています")
            self.warning_label.setStyleSheet("color: red;")
        else:
            self.warning_label.clear()
    
        def execute_rename(self):
            selected_images = self.image_list.get_selected_images()
            if not selected_images:
                QMessageBox.warning(self, "警告", "リネームする画像が選択されていません。")
                return
            
            pattern = self.word_blocks.get_rename_pattern()
            fixed_part, start_number = self.word_blocks.get_sequence_info()
            
            # 複数選択時に連番必須チェック
            if len(selected_images) > 1 and "{連番}" not in pattern:
                QMessageBox.warning(self, "警告", "複数画像のリネームには連番が必要です。")
                return
            
            new_paths = self.renamer.rename_files(selected_images, pattern, self, fixed_part, start_number)
            if new_paths:
                if self.current_folder:
                    self.image_list.load_images(self.current_folder)
                self.preview.clear()

    def open_settings(self):
        print("Opening settings dialog...")
        dialog = SettingsDialog(self)
        dialog.settings_updated.connect(self.refresh_metadata)
        print("Connected settings_updated signal to refresh_metadata")
        dialog.templates_updated.connect(self.word_blocks.refresh_templates)
        print("Connected templates_updated signal to word_blocks.refresh_templates")
        dialog.templates_updated.connect(lambda: print("templates_updated signal received in MainWindow"))
        dialog.exec_()
        print("Settings dialog closed")