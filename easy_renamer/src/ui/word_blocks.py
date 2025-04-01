from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox
from PyQt5.QtCore import Qt

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
        
        # 定型文選択
        self.template_combo = QComboBox()
        self.template_combo.addItems(["出品用_キャラ", "テスト_画像", "カスタム"])
        self.template_combo.currentTextChanged.connect(self.update_pattern)
        
        # 連番設定
        self.sequence_button = QPushButton("連番設定")
        self.sequence_button.clicked.connect(self.add_sequence)
        
        self.layout.addWidget(self.candidates)
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
        # 簡易的な連番挿入（後でsettings_dialogで詳細設定）
        self.pattern_input.insert("{連番:03d}")  # 例: 001, 002, ...
    
    def get_rename_pattern(self):
        return self.pattern_input.text()
