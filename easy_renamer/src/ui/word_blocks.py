from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from core.settings import Settings

class WordBlocks(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.settings = Settings()
        
        self.metadata_candidates = QListWidget()
        self.metadata_candidates.setDragEnabled(True)
        self.metadata_candidates.setAcceptDrops(True)
        self.metadata_candidates.doubleClicked.connect(self.insert_candidate)
        
        self.predefined_candidates = QListWidget()
        self.predefined_candidates.setDragEnabled(True)
        self.predefined_candidates.setAcceptDrops(True)
        self.predefined_candidates.doubleClicked.connect(self.insert_candidate)
        for word in self.settings.get_search_words():
            self.predefined_candidates.addItem(word)
        
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("例: {定型文} {ワード1} {連番}")  # スペースで区切った例に変更
        self.pattern_input.setAcceptDrops(True)
        self.pattern_input.dropEvent = self.drop_event
        
        self.template_combo = QComboBox()
        self.template_combo.addItems(self.settings.get_templates())
        self.template_combo.currentTextChanged.connect(self.update_pattern)
        
        self.sequence_button = QPushButton("連番設定")
        self.sequence_button.clicked.connect(self.add_sequence)
        
        self.layout.addWidget(QLabel("メタデータ一致ワード:"))
        self.layout.addWidget(self.metadata_candidates)
        self.layout.addWidget(QLabel("事前登録ワード:"))
        self.layout.addWidget(self.predefined_candidates)
        self.layout.addWidget(QLabel("リネームパターン:"))
        self.layout.addWidget(self.template_combo)
        self.layout.addWidget(self.pattern_input)
        self.layout.addWidget(self.sequence_button)
    
    def update_candidates(self, metadata):
        self.metadata_candidates.clear()
        for value in metadata.values():
            self.metadata_candidates.addItem(value)
    
    def insert_candidate(self, index):
        item = self.metadata_candidates.itemFromIndex(index) or self.predefined_candidates.itemFromIndex(index)
        if item:
            self.pattern_input.insert(f" {item.text()} ")  # 半角スペースで挟む
    
    def update_pattern(self, template):
        if template != "カスタム":
            self.pattern_input.setText(template)  # デフォルトパターンを削除し、テンプレートのみ
        else:
            self.pattern_input.clear()  # カスタム選択時は空に
    
    def add_sequence(self):
        self.pattern_input.insert(" {連番:03d} ")  # 半角スペースで挟む
    
    def drop_event(self, event):
        data = event.mimeData()
        if data.hasText():
            self.pattern_input.insert(f" {data.text()} ")  # 半角スペースで挟む
        event.accept()
    
    def get_rename_pattern(self):
        return self.pattern_input.text().strip()  # 前後の余分なスペースを削除
