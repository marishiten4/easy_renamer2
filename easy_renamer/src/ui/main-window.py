from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from ui.image_list import ImageList
from ui.preview import Preview
from ui.word_blocks import WordBlocks
from core.renamer import Renamer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Easy Renamer")
        self.resize(800, 600)
        
        # レイアウト設定
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        
        # 左側: 画像リスト
        self.image_list = ImageList()
        self.layout.addWidget(self.image_list, 1)
        
        # 右側: プレビューと操作エリア
        right_layout = QVBoxLayout()
        self.preview = Preview()
        self.word_blocks = WordBlocks()
        self.rename_button = QPushButton("リネーム実行")
        self.folder_button = QPushButton("フォルダ選択")
        
        right_layout.addWidget(self.preview, 2)
        right_layout.addWidget(self.word_blocks, 1)
        right_layout.addWidget(self.folder_button)
        right_layout.addWidget(self.rename_button)
        
        self.layout.addLayout(right_layout, 2)
        
        # イベント接続
        self.folder_button.clicked.connect(self.select_folder)
        self.rename_button.clicked.connect(self.execute_rename)
        self.image_list.itemClicked.connect(self.update_preview)
        
        self.renamer = Renamer()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            self.image_list.load_images(folder)
    
    def update_preview(self, item):
        image_path = item.data(32)  # ユーザー定義データを取得
        self.preview.update_image(image_path)
        metadata = self.renamer.get_metadata(image_path)
        self.word_blocks.update_candidates(metadata)
    
    def execute_rename(self):
        selected_images = self.image_list.selected_images()
        self.renamer.rename_files(selected_images, self.word_blocks.get_rename_pattern())
