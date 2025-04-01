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
                scale_down = min(self.max_pixel_size / final_width, self.max_pixel_size / final_height)  # 括弧を閉じる
                final_width = int(final_width * scale_down)
                final_height = int(final_height * scale_down)
                print(f"Pixel size limited: {final_width}x{final_height}")  # デバッグ出力
            
            scaled_pixmap = scaled_pixmap.scaled(
                final_width,
                final_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            print(f"Scaled pixmap size: {scaled_pixmap.width()}x{scaled_pixmap.height()}")  # デバッグ出力
            self.image_label.setPixmap(scaled_pixmap)
    
    def zoom_in(self):
        print(f"Before zoom_in: scale_factor = {self.scale_factor}")  # デバッグ出力
        # 新しいスケールを計算
        new_scale = self.scale_factor * 1.2
        # 上限チェック
        if new_scale <= self.max_scale:
            self.scale_factor = new_scale
        else:
            self.scale_factor = self.max_scale
            print(f"Maximum scale reached: {self.scale_factor}")
        print(f"After zoom_in: scale_factor = {self.scale_factor}")  # デバッグ出力
        self.update_display()
    
    def zoom_out(self):
        print(f"Before zoom_out: scale_factor = {self.scale_factor}")  # デバッグ出力
        # 新しいスケールを計算
        new_scale = self.scale_factor / 1.2
        # 下限チェック
        if new_scale >= self.min_scale:
            self.scale_factor = new_scale
        else:
            self.scale_factor = self.min_scale
            print(f"Minimum scale reached: {self.scale_factor}")
        print(f"After zoom_out: scale_factor = {self.scale_factor}")  # デバッグ出力
        self.update_display()
    
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
        self.current_pixmap = QPixmap(image_path)
        self.scale_factor = 1.0
        self.update_display()
    
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
    
    def open_zoom_dialog(self):
        if self.current_pixmap:
            dialog = ZoomDialog(self.current_pixmap, self)
            dialog.exec_()
    
    def zoom_out(self):
        if self.scale_factor > self.min_scale:
            self.scale_factor /= 1.2
            self.update_display()
    
    def resizeEvent(self, event):
        self.update_display()
        super().resizeEvent(event)
