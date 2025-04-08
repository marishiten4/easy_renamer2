from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QSize, pyqtSignal
from PyQt5.QtGui import QDrag, QFont, QFontMetrics
from core.settings import Settings
import json
import os

class WordBlocks(QWidget):
    templates_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.settings = Settings()
        self.config_file = "settings.json"
        
        word_blocks_layout = QVBoxLayout()
        font = QFont()
        font.setPointSize(8)
        font_metrics = QFontMetrics(font)
        item_height = font_metrics.height() + 4

        self.word_list = QListWidget()
        self.word_list.setDragEnabled(True)
        self.word_list.setAcceptDrops(True)
        self.word_list.doubleClicked.connect(self.insert_candidate)
        self.word_list.setWordWrap(False)
        self.word_list.setFont(font)
        self.word_list.setStyleSheet(f"""
            QListWidget::item {{ 
                border: 1px solid gray; 
                padding: 4px; 
                margin: 2px; 
                height: {item_height}px; 
            }}
            QListWidget::item:selected {{ 
                background-color: #0078d7; 
                color: white; 
            }}
        """)
        self.word_list.setFlow(QListWidget.LeftToRight)
        self.word_list.setWrapping(True)
        self.word_list.setFixedHeight(100)

        for word in self.settings.get_search_words():
            self.word_list.addItem(word)
        
        self.adjust_item_width(self.word_list)

        word_blocks_layout.addWidget(QLabel("使用可能なワード:"))
        word_blocks_layout.addWidget(self.word_list)
        
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("例: 定型文 ワード1 連番")
        self.pattern_input.setAcceptDrops(True)
        self.pattern_input.dropEvent = self.drop_event
        
        self.template_combo = QComboBox()
        self.template_combo.addItems(self.settings.get_templates())
        self.template_combo.setCurrentIndex(-1)
        self.template_combo.currentTextChanged.connect(self.update_pattern)
        
        # 連番設定（固定部分と開始番号）
        self.sequence_layout = QHBoxLayout()
        self.fixed_part_input = QLineEdit()
        self.fixed_part_input.setPlaceholderText("固定部分 (例: IMG)")
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("開始番号 (例: 001)")
        self.sequence_button = QPushButton("連番追加")
        self.sequence_button.clicked.connect(self.add_sequence)
        self.sequence_position = QCheckBox("先頭に追加")
        
        self.sequence_layout.addWidget(QLabel("連番設定:"))
        self.sequence_layout.addWidget(self.fixed_part_input)
        self.sequence_layout.addWidget(self.number_input)
        self.sequence_layout.addWidget(self.sequence_position)
        self.sequence_layout.addWidget(self.sequence_button)
        
        self.layout.addLayout(word_blocks_layout)
        self.layout.addWidget(QLabel("リネームパターン:"))
        self.layout.addWidget(self.template_combo)
        self.layout.addWidget(self.pattern_input)
        self.layout.addLayout(self.sequence_layout)

        self.templates_updated.connect(self.refresh_templates)

    def adjust_item_width(self, list_widget):
        font_metrics = QFontMetrics(list_widget.font())
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            text = item.text()
            width = font_metrics.width(text) + 20
            height = font_metrics.height() + 8
            item.setSizeHint(QSize(width, height))
    
    def normalize_string(self, s):
        if s and isinstance(s, str):
            return s.strip().lower()
        return ""

    def update_candidates(self, metadata):
        current_words = set()
        for i in range(self.word_list.count()):
            current_words.add(self.word_list.item(i).text())
        
        predefined_words = set(self.settings.get_search_words())
        
        self.word_list.clear()
        for word in predefined_words:
            if word and word.strip():
                self.word_list.addItem(word)
        
        metadata_words = set()
        for key, value in metadata.items():
            if key == "no_match":
                continue
            normalized_value = self.normalize_string(value)
            if (normalized_value and 
                normalized_value not in ["", "none", "null", "n/a", "no match", "一致なし"]):
                metadata_words.add(value.strip())
        
        for value in metadata_words:
            if value not in predefined_words and value not in current_words:
                self.word_list.addItem(value)
        
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
        fixed_part = self.fixed_part_input.text()
        start_number = self.number_input.text() or "1"
        sequence_text = f"{fixed_part}{start_number}"  # 例: gr441
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
    
    def get_sequence_info(self):
        """連番設定（固定部分と開始番号）を返す"""
        return self.fixed_part_input.text(), self.number_input.text() or "001"
    
    def refresh_templates(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        settings_path = os.path.join(base_path, 'settings.json')
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
            templates = settings_data.get('templates', [])
        except (FileNotFoundError, json.JSONDecodeError):
            templates = []

        self.template_combo.clear()
        if not templates:
            self.template_combo.addItem("No templates available")
        else:
            self.template_combo.addItems(templates)
        self.template_combo.setCurrentIndex(-1)