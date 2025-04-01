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
            list_widget.setStyleSheet
