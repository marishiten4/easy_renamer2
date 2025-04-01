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
        item_height = font_metrics.height() + 4

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
                padding: 4px; 
                margin: 2px; 
                height: {item_height}px; 
            }}
            QListWidget::item:selected {{ 
                background-color: #0078d7;  /* 選択時の背景色を青に */
                color: white;               /* 選択時の文字色を白に */
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
        self.sequence_input.setPlaceholderText("連
