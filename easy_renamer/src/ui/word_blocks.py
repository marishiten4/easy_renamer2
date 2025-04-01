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
        item_height = font_metrics.height() + 2  # さらにコンパクトに

        # メタデータ一致ワードと事前登録ワードを複数列で表示
        grid_layout = QGridLayout()
        self.column_count = 3  # 列数を増やす（3列に）

        # メタデータ一致ワード
        self.metadata_lists = []
        for col in range(self.column_count):
            list_widget = QListWidget()
            list_widget.setDragEnabled(True)
            list_widget.setAcceptDrops(True)
            list_widget.doubleClicked.connect(self.insert_candidate)
            list_widget.setWordWrap(False)
            list_widget.setFont(font)
            list_widget.setStyleSheet(f"""
                QListWidget::item {{ 
                    border: 1px solid gray; 
                    padding: 1px; 
                    margin: 1px; 
                    height: {item_height}px; 
                }}
            """)
            list_widget.setFixedHeight(80)  # 高さをさらに小さく
            self.metadata_lists.append(list_widget)
            grid_layout.addWidget(list_widget, 1, col)

        # 事前登録ワード
        self.predefined_lists = []
        for col in range(self.column_count):
            list_widget = QListWidget()
            list_widget.setDragEnabled(True)
            list_widget.setAcceptDrops(True)
            list_widget.doubleClicked.connect(self.insert_candidate)
            list_widget.setWordWrap(False)
            list_widget.setFont(font)
            list_widget.setStyleSheet(f"""
                QListWidget::item {{ 
                    border: 1px solid gray; 
                    padding: 1px; 
                    margin: 1px; 
                    height: {item_height}px; 
                }}
            """)
            list_widget.setFixedHeight(80)
            self.predefined_lists.append(list_widget)
            grid_layout.addWidget(list_widget, 3, col)

        # ラベルを追加
        grid_layout.addWidget(QLabel("メタデータ一致ワード:"), 0, 0, 1, self.column_count)
        grid_layout.addWidget(QLabel("事前登録ワード:"), 2, 0, 1, self.column_count)

        # 事前登録ワードを追加
        for i, word in enumerate(self.settings.get_search_words()):
            col = i % self.column_count
            self.predefined_lists[col].addItem(word)
        
        # 横幅を文字数に応じて調整
        for list_widget in self.metadata_lists + self.predefined_lists:
            self.adjust_item_width(list_widget)

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
            width = font_metrics.width(text) + 10
            max_width = max(max_width, width)
        list_widget.setMinimumWidth(max_width + 20)
    
    def update_candidates(self, metadata):
        # すべてのリストをクリア
        for list_widget in self.metadata_lists:
            list_widget.clear()
        
        # メタデータ一致ワードを列に分配
        for i, value in enumerate(metadata.values()):
            col = i % self.column_count
            self.metadata_lists[col].addItem(value)
        
        # 横幅を再調整
        for list_widget in self.metadata_lists:
            self.adjust_item_width(list_widget)
    
    def insert_candidate(self, index):
        for list_widget in self.metadata_lists + self.predefined_lists:
            item = list_widget.itemFromIndex(index)
            if item:
                self.pattern_input.insert(f" {item.text()} ")
                break
    
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
