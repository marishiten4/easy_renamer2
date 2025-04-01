from PyQt5.QtWidgets import QListWidget, QPushButton, QVBoxLayout, QWidget, QListWidgetItem, QApplication  # QApplicationを追加
from PyQt5.QtCore import pyqtSignal, Qt
import os

class ImageList(QWidget):
    itemClicked = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        
        self.prev_button = QPushButton("前へ")
        self.next_button = QPushButton("次へ")
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.next_button)
        
        self.images = []
        self.page_size = 20
        self.current_page = 0
        self.last_selected = None
        
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.list_widget.itemClicked.connect(self.handle_item_clicked)
    
    def load_images(self, folder):
        self.images = []
        for file in os.listdir(folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.images.append(os.path.join(folder, file))
        self.show_page()
    
    def show_page(self):
        self.list_widget.clear()
        start = self.current_page * self.page_size
        end = min(start + self.page_size, len(self.images))
        for i in range(start, end):
            item = QListWidgetItem(os.path.basename(self.images[i]))
            item.setData(32, self.images[i])
            self.list_widget.addItem(item)
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(end < len(self.images))
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()
    
    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.images):
            self.current_page += 1
            self.show_page()
    
    def handle_item_clicked(self, item):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            if item.isSelected():
                item.setSelected(False)
            else:
                item.setSelected(True)
        elif modifiers == Qt.ShiftModifier and self.last_selected is not None:
            start = self.list_widget.row(self.last_selected)
            end = self.list_widget.row(item)
            for i in range(min(start, end), max(start, end) + 1):
                self.list_widget.item(i).setSelected(True)
        else:
            self.list_widget.clearSelection()
            item.setSelected(True)
            self.last_selected = item
        self.itemClicked.emit(item)
    
    def selected_images(self):
        return [item.data(32) for item in self.list_widget.selectedItems()]
