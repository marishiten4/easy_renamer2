import exifread
from PIL import Image
from core.settings import Settings

class MetadataParser:
    def __init__(self):
        self.settings = Settings()
        self.word_map = self.settings.get_word_map()
    
    def parse(self, image_path):
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
            metadata = {tag: str(tags[tag]) for tag in tags}
            print(f"Raw metadata for {image_path}: {metadata}")  # デバッグ用
            
            translated = {}
            for key, value in metadata.items():
                for en_word, jp_word in self.word_map.items():
                    if en_word in value:
                        translated[en_word] = jp_word
            return translated if translated else {"no_match": "一致なし"}
        except Exception as e:
            print(f"Error parsing metadata for {image_path}: {e}")
            return {"error": str(e)}
