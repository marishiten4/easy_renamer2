from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QDrag, QFont, QFontMetrics
from core.settings import Settings

class WordBlocks(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.settings = Settings()
        
        # ワードブロック全体のレイアウト
        word_blocks_layout = QVBoxLayout()

        # フォント設定
        font = QFont()
        font.setPointSize(8)
        font_metrics = QFontMetrics(font)
        item_height = font_metrics.height() + 2

        # 統合されたワードリスト（メタデータ一致ワードと事前登録ワードを1つに）
        self.word_list = QListWidget()
        self.word_list.setDragEnabled(True)
        self.word_list.setAcceptDrops(True)
        self.word_list.doubleClicked.connect(self.insert_candidate)
        self.word_list.setWordWrap(False)
        self.word_list.setFont(font)
        self.word_list.setStyleSheet(f"""
            QListWidget::item {{ 
                border: 1px solid gray; 
                padding: 2px; 
                margin: 1px; 
                height: {item_height}px; 
            }}
        """)
        # 横並び表示（左から右へ）
        self.word_list.setFlow(QListWidget.LeftToRight)
        self.word_list.setWrapping(True)  # 自動折り返しを有効化
        self.word_list.setFixedHeight(100)  # 高さは適度に

        # 事前登録ワードを追加
        for word in self.settings.get_search_words():
            self.word_list.addItem(word)
        
        # 横幅を文字数に応じて調整
        self.adjust_item_width(self.word_list)

        word_blocks_layout.addWidget(QLabel("使用可能なワード:"))
        word_blocks_layout.addWidget(self.word_list)
        
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
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            text = item.text()
            width = font_metrics.width(text) + 12  # パディングを増やして文字が切れないように
            height = font_metrics.height() + 4  # 高さをフォントサイズに合わせて調整
            item.setSizeHint(QSize(width, height))
    
    def update_candidates(self, metadata):
        # メタデータ一致ワードを追加（既存の事前登録ワードの後に）
        current_count = self.word_list.count()
        for value in metadata.values():
            self.word_list.addItem(value)
        
        # 横幅を再調整
        self.adjust_item_width(self.word_list)
    
    def insert_candidate(self, index):
        item = self.word_list.itemFromIndex(index)
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
