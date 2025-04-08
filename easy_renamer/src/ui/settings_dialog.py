from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QListWidget, QHBoxLayout, QLabel, QScrollArea, QWidget, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFontMetrics
from core.settings import Settings
import logging

logging.basicConfig(level=logging.DEBUG)

class SettingsDialog(QDialog):
    settings_updated = pyqtSignal()
    templates_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.settings = Settings()
        self.layout = QVBoxLayout(self)
        
        # テンプレート設定（省略）
        self.template_list = QListWidget()
        self.template_input = QLineEdit()
        self.template_add_button = QPushButton("追加/編集")
        self.template_remove_button = QPushButton("削除")
        self.template_editing_index = None
        self.template_add_button.clicked.connect(self.add_or_edit_template)
        self.template_remove_button.clicked.connect(self.remove_template)
        self.template_list.doubleClicked.connect(self.copy_template_to_input)
        for template in self.settings.get_templates():
            self.template_list.addItem(template)
        
        template_layout = QVBoxLayout()
        template_buttons = QHBoxLayout()
        template_layout.addWidget(QLabel("定型文:"))
        template_layout.addWidget(self.template_list)
        template_layout.addWidget(self.template_input)
        template_buttons.addWidget(self.template_add_button)
        template_buttons.addWidget(self.template_remove_button)
        template_layout.addLayout(template_buttons)
        
        # 検索用ワード設定
        self.search_words_container = QWidget()
        self.search_words_container.setStyleSheet("background-color: #ffffff; border: none;")
        self.search_words_layout = QVBoxLayout(self.search_words_container)
        self.search_words_layout.setAlignment(Qt.AlignTop)
        self.search_words_layout.setSpacing(2)  # 間隔を小さく
        self.search_words_layout.setContentsMargins(2, 2, 2, 2)
        self.search_input = QLineEdit()
        self.search_add_button = QPushButton("追加/編集")
        self.search_remove_button = QPushButton("削除")
        self.search_editing_index = None
        self.search_add_button.clicked.connect(self.add_or_edit_search_word)
        self.search_remove_button.clicked.connect(self.remove_search_word)
        
        search_layout = QVBoxLayout()
        self.search_scroll = QScrollArea()
        self.search_scroll.setWidgetResizable(True)
        self.search_scroll.setWidget(self.search_words_container)
        self.search_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.search_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.search_scroll.setStyleSheet("QScrollArea { border: 1px solid #a0a0a0; background-color: #ffffff; }")
        search_buttons = QHBoxLayout()
        search_layout.addWidget(QLabel("検索用ワード:"))
        search_layout.addWidget(self.search_scroll)
        search_layout.addWidget(self.search_input)
        search_buttons.addWidget(self.search_add_button)
        search_buttons.addWidget(self.search_remove_button)
        search_layout.addLayout(search_buttons)
        self.load_search_words()
        
        # メタデータ一致ワード設定
        self.word_map_container = QWidget()
        self.word_map_container.setStyleSheet("background-color: #ffffff; border: none;")
        self.word_map_outer_layout = QVBoxLayout(self.word_map_container)
        self.word_map_outer_layout.setAlignment(Qt.AlignTop)
        self.word_map_outer_layout.setSpacing(2)  # 間隔を小さく
        self.word_map_outer_layout.setContentsMargins(2, 2, 2, 2)
        self.word_en_input = QLineEdit()
        self.word_jp_input = QLineEdit()
        self.word_add_button = QPushButton("追加/編集")
        self.word_remove_button = QPushButton("削除")
        self.word_editing_index = None
        self.word_add_button.clicked.connect(self.add_or_edit_word_map)
        self.word_remove_button.clicked.connect(self.remove_word_map)
        
        word_map_layout = QVBoxLayout()
        self.word_map_scroll = QScrollArea()
        self.word_map_scroll.setWidgetResizable(True)
        self.word_map_scroll.setWidget(self.word_map_container)
        self.word_map_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.word_map_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.word_map_scroll.setStyleSheet("QScrollArea { border: 1px solid #a0a0a0; background-color: #ffffff; }")
        word_map_buttons = QHBoxLayout()
        word_map_inputs = QHBoxLayout()
        word_map_layout.addWidget(QLabel("メタデータ一致ワード:"))
        word_map_layout.addWidget(self.word_map_scroll)
        word_map_inputs.addWidget(QLabel("英語:"))
        word_map_inputs.addWidget(self.word_en_input)
        word_map_inputs.addWidget(QLabel("日本語:"))
        word_map_inputs.addWidget(self.word_jp_input)
        word_map_layout.addLayout(word_map_inputs)
        word_map_buttons.addWidget(self.word_add_button)
        word_map_buttons.addWidget(self.word_remove_button)
        word_map_layout.addLayout(word_map_buttons)
        self.load_word_map()
        
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)
        
        self.layout.addLayout(template_layout)
        self.layout.addLayout(search_layout)
        self.layout.addLayout(word_map_layout)
        self.layout.addWidget(self.save_button)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.rearrange_search_words()
        self.rearrange_word_map()

    # テンプレート関連（省略）
    def add_or_edit_template(self):
        template = self.template_input.text()
        if template:
            if self.template_editing_index is not None:
                self.template_list.item(self.template_editing_index).setText(template)
                self.template_editing_index = None
            else:
                self.template_list.addItem(template)
            self.template_input.clear()
    
    def remove_template(self):
        selected = self.template_list.currentItem()
        if selected:
            self.template_list.takeItem(self.template_list.row(selected))
            self.template_editing_index = None
    
    def copy_template_to_input(self):
        selected = self.template_list.currentItem()
        if selected:
            self.template_input.setText(selected.text())
            self.template_editing_index = self.template_list.row(selected)

    # 検索用ワード関連
    def load_search_words(self):
        self.rearrange_search_words()

    def rearrange_search_words(self):
        for i in reversed(range(self.search_words_layout.count())):
            layout = self.search_words_layout.itemAt(i).layout()
            if layout:
                for j in reversed(range(layout.count())):
                    layout.takeAt(j).widget().deleteLater()
                self.search_words_layout.removeItem(layout)
        
        current_row = QHBoxLayout()
        current_row.setAlignment(Qt.AlignLeft)
        current_row.setSpacing(2)  # 間隔を小さく
        self.search_words_layout.addLayout(current_row)
        
        # ビューポートの幅を正確に取得
        viewport_width = self.search_scroll.viewport().width() - 10  # マージン考慮
        if viewport_width <= 0:
            viewport_width = 400  # デフォルト値
        
        for word in self.settings.get_search_words():
            button = QPushButton(word)
            button.setFixedHeight(18)  # 高さを小さく
            button.setStyleSheet("background-color: #ffffff; border: 1px solid #a0a0a0; padding: 0px 2px; margin: 0px;")
            button.clicked.connect(lambda checked, w=word: self.copy_search_word_to_input(w))
            font_metrics = QFontMetrics(button.font())
            text_width = font_metrics.width(word)
            padding = 4  # paddingを小さく
            border = 1  # borderを小さく
            total_width = text_width + padding + border
            button.setFixedWidth(total_width)
            current_row = self.add_widget_to_search_row(button, current_row, viewport_width)
        
        # コンテナの高さを動的に調整
        self.search_words_container.adjustSize()
        total_height = self.search_words_layout.sizeHint().height()
        self.search_words_container.setMinimumHeight(total_height)
        QApplication.processEvents()

    def add_widget_to_search_row(self, widget, current_row, viewport_width):
        total_width = sum(item.widget().width() for item in [current_row.itemAt(i) for i in range(current_row.count())]) + current_row.spacing() * (current_row.count() - 1) if current_row.count() > 0 else 0
        if total_width + widget.width() + current_row.spacing() > viewport_width:
            current_row = QHBoxLayout()
            current_row.setAlignment(Qt.AlignLeft)
            current_row.setSpacing(2)
            self.search_words_layout.addLayout(current_row)
            logging.debug(f"New search row created. Viewport width: {viewport_width}, Total rows: {self.search_words_layout.count()}")
        current_row.addWidget(widget)
        return current_row
    
    def add_or_edit_search_word(self):
        word = self.search_input.text()
        if word:
            if self.search_editing_index is not None:
                self.settings.get_search_words()[self.search_editing_index] = word
            else:
                self.settings.get_search_words().append(word)
            self.rearrange_search_words()
            self.search_input.clear()
            self.search_editing_index = None
    
    def remove_search_word(self):
        if self.search_editing_index is not None:
            self.settings.get_search_words().pop(self.search_editing_index)
            self.rearrange_search_words()
            self.search_editing_index = None
            self.search_input.clear()
    
    def copy_search_word_to_input(self, word):
        self.search_input.setText(word)
        self.search_editing_index = self.settings.get_search_words().index(word)

    # メタデータ一致ワード関連
    def load_word_map(self):
        self.rearrange_word_map()

    def rearrange_word_map(self):
        for i in reversed(range(self.word_map_outer_layout.count())):
            layout = self.word_map_outer_layout.itemAt(i).layout()
            if layout:
                for j in reversed(range(layout.count())):
                    layout.takeAt(j).widget().deleteLater()
                self.word_map_outer_layout.removeItem(layout)
        
        current_row = QHBoxLayout()
        current_row.setAlignment(Qt.AlignLeft)
        current_row.setSpacing(2)  # 間隔を小さく
        self.word_map_outer_layout.addLayout(current_row)
        
        # ビューポートの幅を正確に取得
        viewport_width = self.word_map_scroll.viewport().width() - 10  # マージン考慮
        if viewport_width <= 0:
            viewport_width = 400  # デフォルト値
        
        for en, jp in self.settings.get_word_map().items():
            label = QLabel(f"{en}: {jp}")
            label.setFixedHeight(18)  # 高さを小さく
            label.setStyleSheet("background-color: #ffffff; border: 1px solid #a0a0a0; padding: 0px 2px; margin: 0px;")
            label.mousePressEvent = lambda event, e=en, j=jp: self.copy_word_map_to_input(e, j)
            font_metrics = QFontMetrics(label.font())
            text_width = font_metrics.width(f"{en}: {jp}")
            padding = 4  # paddingを小さく
            border = 1  # borderを小さく
            total_width = text_width + padding + border
            label.setFixedWidth(total_width)
            current_row = self.add_widget_to_word_map_row(label, current_row, viewport_width)
        
        # コンテナの高さを動的に調整
        self.word_map_container.adjustSize()
        total_height = self.word_map_outer_layout.sizeHint().height()
        self.word_map_container.setMinimumHeight(total_height)
        QApplication.processEvents()

    def add_widget_to_word_map_row(self, widget, current_row, viewport_width):
        total_width = sum(item.widget().width() for item in [current_row.itemAt(i) for i in range(current_row.count())]) + current_row.spacing() * (current_row.count() - 1) if current_row.count() > 0 else 0
        if total_width + widget.width() + current_row.spacing() > viewport_width:
            current_row = QHBoxLayout()
            current_row.setAlignment(Qt.AlignLeft)
            current_row.setSpacing(2)
            self.word_map_outer_layout.addLayout(current_row)
            logging.debug(f"New word map row created. Viewport width: {viewport_width}, Total rows: {self.word_map_outer_layout.count()}")
        current_row.addWidget(widget)
        return current_row
    
    def add_or_edit_word_map(self):
        en = self.word_en_input.text()
        jp = self.word_jp_input.text()
        if en and jp:
            if self.word_editing_index is not None:
                del self.settings.get_word_map()[list(self.settings.get_word_map().keys())[self.word_editing_index]]
            self.settings.get_word_map()[en] = jp
            self.rearrange_word_map()
            self.word_en_input.clear()
            self.word_jp_input.clear()
            self.word_editing_index = None
    
    def remove_word_map(self):
        if self.word_editing_index is not None:
            del self.settings.get_word_map()[list(self.settings.get_word_map().keys())[self.word_editing_index]]
            self.rearrange_word_map()
            self.word_editing_index = None
            self.word_en_input.clear()
            self.word_jp_input.clear()
    
    def copy_word_map_to_input(self, en, jp):
        self.word_en_input.setText(en)
        self.word_jp_input.setText(jp)
        self.word_editing_index = list(self.settings.get_word_map().keys()).index(en)
    
    def save_settings(self):
        templates = [self.template_list.item(i).text() for i in range(self.template_list.count())]
        self.settings.config = {
            "templates": templates,
            "search_words": self.settings.get_search_words(),
            "word_map": self.settings.get_word_map()
        }
        self.settings.save_config()
        self.settings_updated.emit()
        self.templates_updated.emit()
        self.accept()

if __name__ == "__main__":
    app = QApplication([])
    dialog = SettingsDialog()
    dialog.show()
    app.exec_()