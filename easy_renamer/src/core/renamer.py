import os
from PyQt5.QtWidgets import QMessageBox
from core.metadata import MetadataParser
from utils.helpers import count_fullwidth_chars

class Renamer:
    def __init__(self):
        self.metadata_parser = MetadataParser()
    
    def update_word_map(self):
        self.metadata_parser.update_word_map()
    
    def get_metadata(self, image_path):
        return self.metadata_parser.parse(image_path)
    
    def rename_files(self, image_paths, pattern, parent=None, fixed_part="", start_number="1"):
        new_names = []
        folder = os.path.dirname(image_paths[0])
        existing_files = set(os.listdir(folder))
        used_names = set()
        
        start_num = int(start_number) if start_number.isdigit() else 1
        base_sequence = f"{fixed_part}{start_number}"
        
        for i, path in enumerate(image_paths):
            metadata = self.get_metadata(path)
            ext = os.path.splitext(path)[1]
            
            sequence = f"{fixed_part}{start_num + i}"
            try:
                if base_sequence in pattern:
                    new_name = pattern.replace(base_sequence, sequence)
                else:
                    new_name = pattern
                new_name = new_name.format(**metadata)
            except KeyError as e:
                new_name = f"{pattern} {sequence}{ext}"
            
            char_count = count_fullwidth_chars(new_name)
            if char_count > 65:
                new_name = f"[文字数オーバー]{new_name[:62]}..."
            
            new_filename = new_name + ext
            new_path = os.path.join(folder, new_filename)
            
            if new_filename in existing_files or new_filename in used_names:
                reply = QMessageBox.question(
                    parent, "確認",
                    f"'{new_filename}' は既に存在するか、今回のリネームで重複します。\n上書きしますか？",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return None
            
            new_names.append((path, new_path))
            used_names.add(new_filename)
        
        # 複数画像の場合のみ実行確認
        if parent and len(image_paths) > 1 and QMessageBox.question(
            parent, "確認",
            f"{len(new_names)}件のリネームを実行しますか？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        ) != QMessageBox.Yes:
            return None
        
        for old_path, new_path in new_names:
            try:
                os.rename(old_path, new_path)
            except OSError as e:
                print(f"Error renaming {old_path} to {new_path}: {e}")
                return None
        
        return [new_path for _, new_path in new_names]