from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QFont, QFontMetrics
from core.settings import Settings

class WordBlocks(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.settings = Settings()
        
        word_blocks_layout = QHBoxLayout()

        # フォントサイズを設定
        font = QFont()
        font.setPointSize(8)
        font_metrics = QFontMetrics(font)
        item_height = font_metrics.height() + 4  # フォントの高さにパディングを追加

        # メタデータ一致ワード
        self.metadata_candidates = QListWidget()
        self.metadata_candidates.setDragEnabled(True)
        self.metadata_candidates.setAcceptDrops(True)
        self.metadata_candidates.doubleClicked.connect(self.insert_candidate)
        self.metadata_candidates.setWordWrap(True)
        self.metadata_candidates.setFont(font)
        self.metadata_candidates.setStyleSheet(f"""
            QListWidget::item {{ 
                border: 1px solid gray; 
                padding: 2px; 
                margin: 1px; 
                height: {item_height}px; 
            }}
        """)
        self.metadata_candidates.setFixedHeight(100)
        self.metadata_candidates.setMinimumWidth(150)

        # 事前登録ワード
        self.predefined_candidates = QListWidget()
        self.predefined_candidates.setDragEnabled(True)
        self.predefined_candidates.setAcceptDrops(True)
        self.predefined_candidates.doubleClicked.connect(self.insert_candidate)
        self.predefined_candidates.setWordWrap(True)
        self.predefined_candidates.setFont(font)
        self.predefined_candidates.setStyleSheet(f"""
            QListWidget::item {{ 
                border: 1px solid gray; 
                padding: 2px; 
                margin: 1px; 
                height: {item_height}px; 
            }}
        """)
        self.predefined_candidates.setFixedHeight(100)
        self.predefined_candidates.setMinimumWidth(150)

        for word in self.settings.get_search_words():
            self.predefined_candidates.addItem(word)
        
        word_blocks_layout.addWidget(QLabel("メタデータ一致ワード:"))
        word_blocks_layout.addWidget(self.metadata_candidates)
        word_blocks_layout.addWidget(QLabel("事前登録ワード:"))
        word_blocks_layout.addWidget(self.predefined_candidates)
        
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("例: {定型文} {ワード1} {連番}")
        self.pattern_input.setAcceptDrops(True)
        self.pattern_input.dropEvent = self.drop_event
        
        self.template_combo = QComboBox()
        self.template_combo.addItems(self.settings.get_templates())
        self.template_combo.currentTextChanged.connect(self.update_pattern)
        
        self.sequence_input = QLineEdit()
        self.sequence_input.setPlaceholderText("連番形式（例: 連番:03d）")
        self.sequence_button = QPushButton("連番追加")
        self.sequence_button.clicked.connect(self.add_sequence)
        self.sequence_position = QCheckBox("先頭に追加")
        
        self.layout.addLayout(word_blocks_layout)
        self.layout.addWidget(QLabel("リネームパターン:"))
        self.layout.addWidget(self.template_combo)
        self.layout.addWidget(self.pattern_input)
        self.layout.addWidget(QLabel("連番設定:"))
        self.layout.addWidget(self.sequence_input)
        self.layout.addWidget(self.sequence_position)
        self.layout.addWidget(self.sequence_button)
    
    def update_candidates(self, metadata):
        self.metadata_candidates.clear()
        for value in metadata.values():
            self.metadata_candidates.addItem(value)
    
    def insert_candidate(self, index):
        item = self.metadata_candidates.itemFromIndex(index) or self.predefined_candidates.itemFromIndex(index)
        if item:
            self.pattern_input.insert(f" {item.text()} ")
    
    def update_pattern(self, template):
        if template != "カスタム":
            self.pattern_input.setText(template)
        else:
            self.pattern_input.clear()
    
    def add_sequence(self):
        sequence = self.sequence_input.text() or "連番:03d"
        sequence_text = f"{{{sequence}}}"
        if self.sequence_position.isChecked():
            current_text = self.pattern_input.text()
            self.pattern_input.setText(f"{sequence_text} {current_text}".strip())
        else:
            self.pattern_input.insert(f" {sequence_text} ")
    
    def drop_event(self, event):
        data = event.mimeData()
        if data.hasText():
            self.pattern_input.insert(f" {data.text()} ")
        event.accept()
    
    def get_rename_pattern(self):
        return self.pattern_input.text().strip()
