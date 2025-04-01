from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QListWidget, QHBoxLayout
from core.settings import Settings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.settings = Settings()
        self.layout = QVBoxLayout(self)
        
        # 定型文設定
        self.template_list = QListWidget()
        self.template_input = QLineEdit()
        self.template_add_button = QPushButton("追加")
        self.template_add_button.clicked.connect(self.add_template)
        for template in self.settings.get_templates():
            self.template_list.addItem(template)
        
        template_layout = QVBoxLayout()
        template_layout.addWidget(QListWidgetItem("定型文:"))
        template_layout.addWidget(self.template_list)
        template_layout.addWidget(self.template_input)
        template_layout.addWidget(self.template_add_button)
        
        # 検索用ワード設定
        self.search_list = QListWidget()
        self.search_input = QLineEdit()
        self.search_add_button = QPushButton("追加")
        self.search_add_button.clicked.connect(self.add_search_word)
        for word in self.settings.get_search_words():
            self.search_list.addItem(word)
        
        search_layout = QVBoxLayout()
        search_layout.addWidget(QListWidgetItem("検索用ワード:"))
        search_layout.addWidget(self.search_list)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_add_button)
        
        # メタデータ一致ワード設定
        self.word_map_form = QFormLayout()
        self.word_inputs = {}
        for en, jp in self.settings.get_word_map().items():
            input_field = QLineEdit(jp)
            self.word_inputs[en] = input_field
            self.word_map_form.addRow(en, input_field)
        
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)
        
        self.layout.addLayout(template_layout)
        self.layout.addLayout(search_layout)
        self.layout.addLayout(self.word_map_form)
        self.layout.addWidget(self.save_button)
    
    def add_template(self):
        template = self.template_input.text()
        if template:
            self.template_list.addItem(template)
            self.template_input.clear()
    
    def add_search_word(self):
        word = self.search_input.text()
        if word:
            self.search_list.addItem(word)
            self.search_input.clear()
    
    def save_settings(self):
        templates = [self.template_list.item(i).text() for i in range(self.template_list.count())]
        search_words = [self.search_list.item(i).text() for i in range(self.search_list.count())]
        word_map = {en: input_field.text() for en, input_field in self.word_inputs.items()}
        
        self.settings.config = {
            "templates": templates,
            "search_words": search_words,
            "word_map": word_map
        }
        self.settings.save_config()
        self.accept()
