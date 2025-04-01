import os
from core.metadata import MetadataParser

class Renamer:
    def __init__(self):
        self.metadata_parser = MetadataParser()
    
    def get_metadata(self, image_path):
        return self.metadata_parser.parse(image_path)
    
    def rename_files(self, image_paths, pattern):
        for path in image_paths:
            metadata = self.get_metadata(path)
            new_name = pattern.format(**metadata)
            if len(new_name) > 65:  # 全角65文字制限の簡易チェック
                print(f"警告: {new_name} が文字数オーバー")
            new_path = os.path.join(os.path.dirname(path), new_name + os.path.splitext(path)[1])
            os.rename(path, new_path)
