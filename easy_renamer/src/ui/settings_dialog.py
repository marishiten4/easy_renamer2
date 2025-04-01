from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout
from core.settings import Settings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.settings = Settings()
        self.layout = QVBoxLayout(self)
        
        # ワードマップ入力
        self.form_layout = QFormLayout()
        self.word_inputs = {}
        for en, jp in self.settings.load_word_map().items():
            input_field = QLineEdit(jp)
            self.word_inputs[en] = input_field
            self.form_layout.addRow(en, input_field)
        
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)
        
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
    
    def save_settings(self):
        word_map = {en: input_field.text() for en, input_field in self.word_inputs.items()}
        self.settings.save_word_map(word_map)
        self.accept()
