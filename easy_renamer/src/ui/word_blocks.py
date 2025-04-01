from PyQt5.QtWidgets import QListWidget, QLineEdit, QVBoxLayout, QWidget

class WordBlocks(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.candidates = QListWidget()
        self.pattern_input = QLineEdit()
        self.layout.addWidget(self.candidates)
        self.layout.addWidget(self.pattern_input)
    
    def update_candidates(self, metadata):
        self.candidates.clear()
        for key, value in metadata.items():
            self.candidates.addItem(f"{key}: {value}")
    
    def get_rename_pattern(self):
        return self.pattern_input.text()
