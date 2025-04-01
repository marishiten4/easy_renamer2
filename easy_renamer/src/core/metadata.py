import exifread
from PIL import Image
from core.settings import Settings

class MetadataParser:
    def __init__(self):
        self.settings = Settings()
        self.word_map = self.settings.get_word_map()  # "load_word_map" を "get_word_map" に変更
    
    def parse(self, image_path):
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
        metadata = {tag: str(tags[tag]) for tag in tags}
        
        # メタデータをワードマップで変換
        translated = {}
        for key, value in metadata.items():
            for en_word, jp_word in self.word_map.items():
                if en_word in value:
                    translated[en_word] = jp_word
        return translated if translated else metadata
