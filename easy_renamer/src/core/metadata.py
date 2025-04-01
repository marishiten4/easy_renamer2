from PIL import Image
import os
from core.settings import Settings

class MetadataParser:
    def __init__(self):
        self.settings = Settings()
        self.word_map = self.settings.get_word_map()
    
    def parse(self, image_path):
        try:
            # PILでメタデータを取得
            with Image.open(image_path) as img:
                metadata = img.info
            print(f"Raw metadata from PIL for {image_path}: {metadata}")
            
            translated = {}
            for key, value in metadata.items():
                if isinstance(value, str):
                    for en_word, jp_word in self.word_map.items():
                        if en_word in value:
                            translated[en_word] = jp_word
            
            # メタデータが空の場合、ファイル名から推測
            if not translated:
                filename = os.path.splitext(os.path.basename(image_path))[0]
                print(f"Extracting from filename: {filename}")
                for en_word, jp_word in self.word_map.items():
                    if en_word in filename:
                        translated[en_word] = jp_word
            
            return translated if translated else {"no_match": "一致なし"}
        except Exception as e:
            print(f"Error parsing metadata for {image_path}: {e}")
            return {"error": str(e)}
