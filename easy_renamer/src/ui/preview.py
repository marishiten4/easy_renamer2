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
        self.max_pixel_size = 10000  # ピクセルサイズの上限（幅または高さがこの値を超えないように）
        
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        
        self.update_display()
        self.resize(600, 600)
    
    def update_display(self):
        if self.current_pixmap:
            print(f"Updating display with scale_factor: {self.scale_factor}")  # デバッグ出力
            label_size = self.image_label.size()
            # まずウィジェットのサイズに合わせてスケーリング
            scaled_pixmap = self.current_pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            # スケールファクターを適用
            final_width = int(scaled_pixmap.width() * self.scale_factor)
            final_height = int(scaled_pixmap.height() * self.scale_factor)
            
            # ピクセルサイズが上限を超えないように制限
            if final_width > self.max_pixel_size or final_height > self.max_pixel_size:
                scale_down = min(self.max_pixel
