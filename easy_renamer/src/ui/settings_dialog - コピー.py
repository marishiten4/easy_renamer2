from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QListWidget, QHBoxLayout, QLabel, QScrollArea, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from core.settings import Settings

class SettingsDialog(QDialog):
    settings_updated = pyqtSignal()
    templates_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.settings = Settings()
        self.layout = QVBoxLayout(self)
        
        # テンプレート設定
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
        
        # 検索用ワード設定（ワードブロック形式、横並び＋縦スクロール）
        self.search_words_container = QWidget()
        self.search_words_container.setStyleSheet("background-color: #ffffff;")  # コンテナ背景を白に
        self.search_words_layout = QHBoxLayout(self.search_words_container)
        self.search_words_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.search_words_layout.setSpacing(4)
        self.search_words_layout.setContentsMargins(2, 2, 2, 2)
        self.search_input = QLineEdit()
        self.search_add_button = QPushButton("追加/編集")
        self.search_remove_button = QPushButton("削除")
        self.search_editing_index = None
        self.search_add_button.clicked.connect(self.add_or_edit_search_word)
        self.search_remove_button.clicked.connect(self.remove_search_word)
        self.load_search_words()
        
        search_layout = QVBoxLayout()
        search_scroll = QScrollArea()
        search_scroll.setWidgetResizable(True)
        search_scroll.setWidget(self.search_words_container)
        search_scroll.setContentsMargins(0, 0, 0, 0)
        search_scroll.viewport().setStyleSheet("background-color: #ffffff;")  # ビューポートの背景を白に
        search_buttons = QHBoxLayout()
        search_layout.addWidget(QLabel("検索用ワード:"))
        search_layout.addWidget(search_scroll)
        search_layout.addWidget(self.search_input)
        search_buttons.addWidget(self.search_add_button)
        search_buttons.addWidget(self.search_remove_button)
        search_layout.addLayout(search_buttons)
        
        # メタデータ一致ワード設定（横並び＋縦スクロール）
        self.word_map_container = QWidget()
        self.word_map_container.setStyleSheet("background-color: #ffffff;")  # コンテナ背景を白に
        self.word_map_outer_layout = QVBoxLayout(self.word_map_container)
        self.word_map_outer_layout.setAlignment(Qt.AlignTop)
        self.word_map_outer_layout.setSpacing(4)
        self.word_map_outer_layout.setContentsMargins(2, 2, 2, 2)
        self.word_en_input = QLineEdit()
        self.word_jp_input = QLineEdit()
        self.word_add_button = QPushButton("追加/編集")
        self.word_remove_button = QPushButton("削除")
        self.word_editing_index = None
        self.word_add_button.clicked.connect(self.add_or_edit_word_map)
        self.word_remove_button.clicked.connect(self.remove_word_map)
        self.load_word_map()
        
        word_map_layout = QVBoxLayout()
        word_map_scroll = QScrollArea()
        word_map_scroll.setWidgetResizable(True)
        word_map_scroll.setWidget(self.word_map_container)
        word_map_scroll.setContentsMargins(0, 0, 0, 0)
        word_map_scroll.viewport().setStyleSheet("background-color: #ffffff;")  # ビューポートの背景を白に
        word_map_buttons = QHBoxLayout()
        word_map_inputs = QHBoxLayout()
        word_map_layout.addWidget(QLabel("メタデータ一致ワード:"))
        word_map_layout.addWidget(word_map_scroll)
        word_map_inputs.addWidget(QLabel("英語:"))
        word_map_inputs.addWidget(self.word_en_input)
        word_map_inputs.addWidget(QLabel("日本語:"))
        word_map_inputs.addWidget(self.word_jp_input)
        word_map_layout.addLayout(word_map_inputs)
        word_map_buttons.addWidget(self.word_add_button)
        word_map_buttons.addWidget(self.word_remove_button)
        word_map_layout.addLayout(word_map_buttons)
        
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)
        
        self.layout.addLayout(template_layout)
        self.layout.addLayout(search_layout)
        self.layout.addLayout(word_map_layout)
        self.layout.addWidget(self.save_button)
    
    # テンプレート関連
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
        for word in self.settings.get_search_words():
            button = QPushButton(word)
            button.setFixedHeight(20)
            button.setMinimumWidth(0)
            button.setStyleSheet("background-color: #ffffff; border: 1px solid #a0a0a0; padding: 1px 2px; margin: 0px;")
            button.clicked.connect(lambda checked, w=word: self.copy_search_word_to_input(w))
            self.search_words_layout.addWidget(button)
    
    def add_or_edit_search_word(self):
        word = self.search_input.text()
        if word:
            if self.search_editing_index is not None:
                button = self.search_words_layout.itemAt(self.search_editing_index).widget()
                button.setText(word)
                button.clicked.disconnect()
                button.clicked.connect(lambda checked, w=word: self.copy_search_word_to_input(w))
                self.search_editing_index = None
            else:
                button = QPushButton(word)
                button.setFixedHeight(20)
                button.setMinimumWidth(0)
                button.setStyleSheet("background-color: #ffffff; border: 1px solid #a0a0a0; padding: 1px 2px; margin: 0px;")
                button.clicked.connect(lambda checked, w=word: self.copy_search_word_to_input(w))
                self.search_words_layout.addWidget(button)
            self.search_input.clear()
    
    def remove_search_word(self):
        if self.search_editing_index is not None:
            item = self.search_words_layout.takeAt(self.search_editing_index)
            if item:
                item.widget().deleteLater()
            self.search_editing_index = None
            self.search_input.clear()
    
    def copy_search_word_to_input(self, word):
        self.search_input.setText(word)
        for i in range(self.search_words_layout.count()):
            if self.search_words_layout.itemAt(i).widget().text() == word:
                self.search_editing_index = i
                break
    
    # メタデータ一致ワード関連
    def load_word_map(self):
        word_map = self.settings.get_word_map()
        inner_layout = QHBoxLayout()
        inner_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        inner_layout.setSpacing(4)
        inner_layout.setContentsMargins(2, 2, 2, 2)
        for en, jp in word_map.items():
            label = QLabel(f"{en}: {jp}")
            label.setStyleSheet("background-color: #ffffff; border: 1px solid #a0a0a0; padding: 1px 2px; margin: 0px;")
            label.mousePressEvent = lambda event, e=en, j=jp: self.copy_word_map_to_input(e, j)
            inner_layout.addWidget(label)
        self.word_map_outer_layout.addLayout(inner_layout)
    
    def add_or_edit_word_map(self):
        en = self.word_en_input.text()
        jp = self.word_jp_input.text()
        if en and jp:
            if self.word_editing_index is not None:
                inner_layout = self.word_map_outer_layout.itemAt(0).layout()
                label = inner_layout.itemAt(self.word_editing_index).widget()
                label.setText(f"{en}: {jp}")
                label.mousePressEvent = lambda event, e=en, j=jp: self.copy_word_map_to_input(e, j)
                self.word_editing_index = None
            else:
                inner_layout = self.word_map_outer_layout.itemAt(0).layout() if self.word_map_outer_layout.count() > 0 else QHBoxLayout()
                inner_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                inner_layout.setSpacing(4)
                inner_layout.setContentsMargins(2, 2, 2, 2)
                label = QLabel(f"{en}: {jp}")
                label.setStyleSheet("background-color: #ffffff; border: 1px solid #a0a0a0; padding: 1px 2px; margin: 0px;")
                label.mousePressEvent = lambda event, e=en, j=jp: self.copy_word_map_to_input(e, j)
                inner_layout.addWidget(label)
                if self.word_map_outer_layout.count() == 0:
                    self.word_map_outer_layout.addLayout(inner_layout)
            self.word_en_input.clear()
            self.word_jp_input.clear()
    
    def remove_word_map(self):
        if self.word_editing_index is not None and self.word_map_outer_layout.count() > 0:
            inner_layout = self.word_map_outer_layout.itemAt(0).layout()
            item = inner_layout.takeAt(self.word_editing_index)
            if item:
                item.widget().deleteLater()
            self.word_editing_index = None
            self.word_en_input.clear()
            self.word_jp_input.clear()
    
    def copy_word_map_to_input(self, en, jp):
        self.word_en_input.setText(en)
        self.word_jp_input.setText(jp)
        if self.word_map_outer_layout.count() > 0:
            inner_layout = self.word_map_outer_layout.itemAt(0).layout()
            for i in range(inner_layout.count()):
                label = inner_layout.itemAt(i).widget()
                if label.text() == f"{en}: {jp}":
                    self.word_editing_index = i
                    break
    
    def save_settings(self):
        templates = [self.template_list.item(i).text() for i in range(self.template_list.count())]
        search_words = [self.search_words_layout.itemAt(i).widget().text() for i in range(self.search_words_layout.count())]
        word_map = {}
        if self.word_map_outer_layout.count() > 0:
            inner_layout = self.word_map_outer_layout.itemAt(0).layout()
            for i in range(inner_layout.count()):
                en, jp = inner_layout.itemAt(i).widget().text().split(": ", 1)
                word_map[en] = jp
        
        self.settings.config = {
            "templates": templates,
            "search_words": search_words,
            "word_map": word_map
        }
        print(f"Saving settings: {self.settings.config}")
        self.settings.save_config()
        self.settings_updated.emit()
        print("Emitted settings_updated signal")
        self.templates_updated.emit()
        print("Emitted templates_updated signal")
        self.accept()