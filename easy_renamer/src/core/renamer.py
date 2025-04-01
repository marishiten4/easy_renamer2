import os
from PyQt5.QtWidgets import QMessageBox
from core.metadata import MetadataParser
from utils.helpers import count_fullwidth_chars

class Renamer:
    def __init__(self):
        self.metadata_parser = MetadataParser()
    
    def get_metadata(self, image_path):
        return self.metadata_parser.parse(image_path)
    
    def rename_files(self, image_paths, pattern, parent=None):
        new_names = []
        for i, path in enumerate(image_paths):
            metadata = self.get_metadata(path)
            sequence_format = "{:03d}"  # デフォルト
            if "{連番:" in pattern:
                start = pattern.index("{連番:") + 6
                end = pattern.index("}", start)
                sequence_format = pattern[start:end]
                pattern = pattern.replace(f"{{連番:{sequence_format}}}", "{連番}")
            metadata["連番"] = format(i + 1, sequence_format)
            try:
                new_name = pattern.format(**metadata)
            except KeyError as e:
                new_name = f"[エラー: {e}]" + os.path.basename(path)
            char_count = count_fullwidth_chars(new_name)
            if char_count > 65:
                new_name = f"[文字数オーバー]{new_name[:62]}..."
            new_names.append((path, new_name + os.path.splitext(path)[1]))
        
        if parent and QMessageBox.question(parent, "確認", f"{len(new_names)}件のリネームを実行しますか？") != QMessageBox.Yes:
            return
        
        for old_path, new_name in new_names:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
