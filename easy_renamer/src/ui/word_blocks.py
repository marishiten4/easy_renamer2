from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QCheckBox, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QFont, QFontMetrics
from core.settings import Settings

class WordBlocks(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.settings = Settings()
        
        # ワードブロック全体のレイアウト（横並び）
        word_blocks_layout = QHBoxLayout()

        # フォント設定
        font = QFont()
        font.setPointSize(8)
        font_metrics = QFontMetrics(font)
        item_height = font_metrics.height() + 4

        # メタデータ一致ワード（グリッドレイアウトで複数列表示）
        metadata_layout = QVBoxLayout()
        metadata_label = QLabel("メタデータ一致ワード:")
        self.metadata_candidates = QListWidget()
        self.metadata_candidates.setDragEnabled(True)
        self.metadata_candidates.setAcceptDrops(True)
        self.metadata_candidates.doubleClicked.connect(self.insert_candidate)
        self.metadata_candidates.setWordWrap(False)  # 折り返しを無効化
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
        metadata_layout.addWidget(metadata_label)
        metadata_layout.addWidget(self.metadata_candidates)

        # 事前登録ワード（グリッドレイアウトで複数列表示）
        predefined_layout = QVBoxLayout()
        predefined_label = QLabel("事前登録ワード:")
        self.predefined_candidates = QListWidget()
        self.predefined_candidates.setDragEnabled(True)
        self.predefined_candidates.setAcceptDrops(True)
        self.predefined_candidates.doubleClicked.connect(self.insert_candidate)
        self.predefined_candidates.setWordWrap(False)
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
        predefined_layout.addWidget(predefined_label)
        predefined_layout.addWidget(self.predefined_candidates)

        # ワードをグリッドレイアウトで複数列に配置
        grid_layout = QGridLayout()
        grid_layout.addLayout(metadata_layout, 0, 0)
        grid_layout.addLayout(predefined_layout, 0, 1)

        # 事前登録ワードを追加
        for word in self.settings.get_search_words():
            self.predefined_candidates.addItem(word)
        
        # 横幅を文字数に応じて調整
        self.adjust_item_width(self.metadata_candidates)
        self.adjust_item_width(self.predefined_candidates)

        word_blocks_layout.addLayout(grid_layout)
        
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
    
    def adjust_item_width(self, list_widget):
        """リストウィジェットのアイテムの幅を文字数に応じて調整"""
        font_metrics = QFontMetrics(list_widget.font())
        max_width = 0
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            text = item.text()
            # 文字数に応じた幅を計算（全角文字を考慮）
            width = font_metrics.width(text) + 10  # パディングを追加
            max_width = max(max_width, width)
        list_widget.setMinimumWidth(max_width + 20)  # スクロールバー分を考慮
    
    def update_candidates(self, metadata):
        self.metadata_candidates.clear()
        for value in metadata.values():
            self.metadata_candidates.addItem(value)
        self.adjust_item_width(self.metadata_candidates)
    
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
