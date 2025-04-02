from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QListWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from core.settings import Settings

class SettingsDialog(QDialog):
    settings_updated = pyqtSignal()
    templates_updated = pyqtSignal()  # テンプレート更新用のシグナル

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.settings = Settings()
        self.layout = QVBoxLayout(self)
        
        self.template_list = QListWidget()
        self.template_input = QLineEdit()
        self.template_add_button = QPushButton("追加")
        self.template_remove_button = QPushButton("削除")
        self.template_add_button.clicked.connect(self.add_template)
        self.template_remove_button.clicked.connect(self.remove_template)
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
        
        self.search_list = QListWidget()
        self.search_input = QLineEdit()
        self.search_add_button = QPushButton("追加")
        self.search_remove_button = QPushButton("削除")
        self.search_add_button.clicked.connect(self.add_search_word)
        self.search_remove_button.clicked.connect(self.remove_search_word)
        for word in self.settings.get_search_words():
            self.search_list.addItem(word)
        
        search_layout = QVBoxLayout()
        search_buttons = QHBoxLayout()
        search_layout.addWidget(QLabel("検索用ワード:"))
        search_layout.addWidget(self.search_list)
        search_layout.addWidget(self.search_input)
        search_buttons.addWidget(self.search_add_button)
        search_buttons.addWidget(self.search_remove_button)
        search_layout.addLayout(search_buttons)
        
        self.word_map_list = QListWidget()
        self.word_en_input = QLineEdit()
        self.word_jp_input = QLineEdit()
        self.word_add_button = QPushButton("追加")
        self.word_remove_button = QPushButton("削除")
        self.word_add_button.clicked.connect(self.add_word_map)
        self.word_remove_button.clicked.connect(self.remove_word_map)
        for en, jp in self.settings.get_word_map().items():
            self.word_map_list.addItem(f"{en}: {jp}")
        
        word_map_layout = QVBoxLayout()
        word_map_buttons = QHBoxLayout()
        word_map_layout.addWidget(QLabel("メタデータ一致ワード:"))
        word_map_layout.addWidget(self.word_map_list)
        word_map_inputs = QHBoxLayout()
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
    
    def add_template(self):
        template = self.template_input.text()
        if template:
            self.template_list.addItem(template)
            self.template_input.clear()
    
    def remove_template(self):
        selected = self.template_list.currentItem()
        if selected:
            self.template_list.takeItem(self.template_list.row(selected))
    
    def add_search_word(self):
        word = self.search_input.text()
        if word:
            self.search_list.addItem(word)
            self.search_input.clear()
    
    def remove_search_word(self):
        selected = self.search_list.currentItem()
        if selected:
            self.search_list.takeItem(self.search_list.row(selected))
    
    def add_word_map(self):
        en = self.word_en_input.text()
        jp = self.word_jp_input.text()
        if en and jp:
            self.word_map_list.addItem(f"{en}: {jp}")
            self.word_en_input.clear()
            self.word_jp_input.clear()
    
    def remove_word_map(self):
        selected = self.word_map_list.currentItem()
        if selected:
            self.word_map_list.takeItem(self.word_map_list.row(selected))
    
    def save_settings(self):
        templates = [self.template_list.item(i).text() for i in range(self.template_list.count())]
        search_words = [self.search_list.item(i).text() for i in range(self.search_list.count())]
        word_map = {}
        for i in range(self.word_map_list.count()):
            item = self.word_map_list.item(i).text()
            en, jp = item.split(": ", 1)
            word_map[en] = jp
        
        self.settings.config = {
            "templates": templates,
            "search_words": search_words,
            "word_map": word_map
        }
        self.settings.save_config()
        self.settings_updated.emit()
        self.accept()
