from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ZoomDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("拡大プレビュー")
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.zoom_in_button = QPushButton("拡大")
        self.zoom_out_button = QPushButton("縮小")
        
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.zoom_in_button)
        self.layout.addWidget(self.zoom_out_button)
        
        self.current_pixmap = pixmap
        self.scale_factor = 1.0
        self.max_scale = 5.0  # 拡大上限
        self.min_scale = 0.2  # 縮小下限
        
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        
        self.update_display()
        self.resize(600, 600)
    
    def update_display(self):
        if self.current_pixmap:
            label_size = self.image_label.size()
            scaled_pixmap = self.current_pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            scaled_pixmap = scaled_pixmap.scaled(
                int(scaled_pixmap.width() * self.scale_factor),
                int(scaled_pixmap.height() * self.scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def zoom_in(self):
        # 拡大上限を厳密にチェック
        if self.scale_factor < self.max_scale:
            self.scale_factor *= 1.2
            if self.scale_factor > self.max_scale:
                self.scale_factor = self.max_scale  # 上限を超えないように調整
            self.update_display()
        else:
            print(f"Maximum scale reached: {self.scale_factor}")
    
    def zoom_out(self):
        # 縮小下限を厳密にチェック
        if self.scale_factor > self.min_scale:
            self.scale_factor /= 1.2
            if self.scale_factor < self.min_scale:
                self.scale_factor = self.min_scale  # 下限を下回らないように調整
            self.update_display()
        else:
            print(f"Minimum scale reached: {self.scale_factor}")
    
    def resizeEvent(self, event):
        self.update_display()
        super().resizeEvent(event)

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel()
        self.image_label.setScaledContents(False)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.zoom_in_button = QPushButton("拡大")
        self.zoom_out_button = QPushButton("縮小")
        
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.zoom_in_button)
        self.layout.addWidget(self.zoom_out_button)
        
        self.current_pixmap = None
        self.scale_factor = 1.0
        self.max_scale = 5.0
        self.min_scale = 0.2
        
        self.zoom_in_button.clicked.connect(self.open_zoom_dialog)
        self.zoom_out_button.clicked.connect(self.zoom_out)
    
    def update_image(self, image_path):
        self.current_pixmap = QPixmap(image
