from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class Preview(QLabel):
    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
    
    def update_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap.scaled(300, 300, aspectRatioMode=1))
