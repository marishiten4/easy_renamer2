from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel()
        # setScaledContents を False に設定して引き延ばしを防ぐ
        self.image_label.setScaledContents(False)
        # 画像を中央に配置
        self.image_label.setAlignment(Qt.AlignCenter)
        self.zoom_in_button = QPushButton("拡大")
        self.zoom_out_button = QPushButton("縮小")
        
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.zoom_in_button)
        self.layout.addWidget(self.zoom_out_button)
        
        self.current_pixmap = None
        self.scale_factor = 1.0
        
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
    
    def update_image(self, image_path):
        self.current_pixmap = QPixmap(image_path)
        self.scale_factor = 1.0
        self.update_display()
    
    def update_display(self):
        if self.current_pixmap:
            # ウィジェットのサイズに合わせてスケーリング（アスペクト比を保持）
            label_size = self.image_label.size()
            scaled_pixmap = self.current_pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            # スケールファクターを適用
            scaled_pixmap = scaled_pixmap.scaled(
                int(scaled_pixmap.width() * self.scale_factor),
                int(scaled_pixmap.height() * self.scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def zoom_in(self):
        self.scale_factor *= 1.2
        self.update_display()
    
    def zoom_out(self):
        self.scale_factor /= 1.2
        self.update_display()
    
    def resizeEvent(self, event):
        # ウィジェットのサイズが変更されたときに再描画
        self.update_display()
        super().resizeEvent(event)
