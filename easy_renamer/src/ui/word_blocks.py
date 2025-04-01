from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel  # QLabelを追加
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class WordBlocks(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # 候補ワードエリア
        self.candidates = QListWidget()
        self.candidates.setDragEnabled(True)
        self.candidates.setAcceptDrops(True)
        self.candidates.doubleClicked.connect(self.insert_candidate)
        
        # リネームパターン入力
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("例: {定型文}_{ワード1}_{連番}")
        self.pattern_input.setAcceptDrops(True)
        self.pattern_input.dropEvent = self.drop_event
        
        # 定型文選択
        self.template_combo = QComboBox()
        self.template_combo.addItems(["出品用_キャラ", "テスト_画像", "カスタム"])
        self.template_combo.currentTextChanged.connect(self.update_pattern)
        
        # 連番設定
        self.sequence_button = QPushButton("連番設定")
        self.sequence_button.clicked.connect(self.add_sequence)
        
        self.layout.addWidget(QLabel("候補ワード:"))  # ここでQLabelを使用
        self.layout.addWidget(self.candidates)
        self.layout.addWidget(QLabel("リネームパターン:"))  # ここでも使用
        self.layout.addWidget(self.template_combo)
        self.layout.addWidget(self.pattern_input)
        self.layout.addWidget(self.sequence_button)
    
    def update_candidates(self, metadata):
        self.candidates.clear()
        for key, value in metadata.items():
            self.candidates.addItem(f"{key}: {value}")
    
    def insert_candidate(self, index):
        item = self.candidates.itemFromIndex(index)
        if item:
            self.pattern_input.insert(item.text().split(": ")[1])
    
    def update_pattern(self, template):
        if template != "カスタム":
            self.pattern_input.setText(f"{template}_{{ワード1}}_{{連番}}")
    
    def add_sequence(self):
        self.pattern_input.insert("{連番:03d}")
    
    def drop_event(self, event):
        data = event.mimeData()
        if data.hasText():
            self.pattern_input.insert(data.text().split(": ")[1])
        event.accept()
    
    def get_rename_pattern(self):
        return self.pattern_input.text()
