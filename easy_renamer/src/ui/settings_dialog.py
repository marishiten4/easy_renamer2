from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import pyqtSignal
from core.settings import Settings

class SettingsDialog(QDialog):
    settings_updated = pyqtSignal()
    templates_updated = pyqtSignal()  # テンプレート更新用のシグナル

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
        self.layout = QVBoxLayout(self)
        
        # 検索ワード入力
        self.search_word_input = QLineEdit()
        self.search_word_input.setPlaceholderText("検索ワードを入力（カンマ区切り）")
        self.search_word_input.setText(", ".join(self.settings.get_search_words()))
        self.layout.addWidget(QLabel("検索ワード:"))
        self.layout.addWidget(self.search_word_input)
        
        # テンプレート入力
        self.template_input = QLineEdit()
        self.template_input.setPlaceholderText("テンプレートを入力（カンマ区切り）")
        self.template_input.setText(", ".join(self.settings.get_templates()))
        self.layout.addWidget(QLabel("リネームテンプレート:"))
        self.layout.addWidget(self.template_input)
        
        # 保存ボタン
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)
    
    def save_settings(self):
        # 検索ワードを保存
        search_words = [word.strip() for word in self.search_word_input.text().split(",") if word.strip()]
        self.settings.set_search_words(search_words)
        
        # テンプレートを保存
        templates = [template.strip() for template in self.template_input.text().split(",") if template.strip()]
        self.settings.set_templates(templates)
        
        self.settings.save()
        self.settings_updated.emit()
        self.templates_updated.emit()  # テンプレート更新シグナルを発信
        self.accept()
