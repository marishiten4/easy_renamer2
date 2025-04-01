from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.zoom_in_button = QPushButton("拡大")  # 「ズームイン」から「拡大」に変更
        self.zoom_out_button = QPushButton("縮小")  # 「ズームアウト」から「縮小」に変更
        
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
            scaled_pixmap = self.current_pixmap.scaled(
                int(150 * self.scale_factor),  # 初期サイズを150x150に縮小
                int(150 * self.scale_factor),
                Qt.KeepAspectRatio
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def zoom_in(self):
        self.scale_factor *= 1.2
        self.update_display()
    
    def zoom_out(self):
        self.scale_factor /= 1.2
        self.update_display()
