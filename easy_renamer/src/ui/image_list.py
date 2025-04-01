from PyQt5.QtWidgets import QListWidget

class ImageList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QListWidget.MultiSelection)
    
    def load_images(self, folder):
        self.clear()
        import os
        for file in os.listdir(folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                item = QListWidgetItem(file)
                item.setData(32, os.path.join(folder, file))  # フルパスを保存
                self.addItem(item)
    
    def selected_images(self):
        return [item.data(32) for item in self.selectedItems()]
