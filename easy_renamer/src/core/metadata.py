from PIL import Image
import os
from core.settings import Settings

class MetadataParser:
    def __init__(self):
        self.settings = Settings()
        self.word_map = self.settings.get_word_map()
    
    def update_word_map(self):
        """設定変更後にword_mapを更新"""
        self.word_map = self.settings.get_word_map()
        print(f"Updated word_map: {self.word_map}")
    
    def parse(self, image_path):
        try:
            with Image.open(image_path) as img:
                metadata = img.info
            print(f"Raw metadata from PIL for {image_path}: {metadata}")
            
            translated = {}
            for key, value in metadata.items():
                if key == 'exif' and isinstance(value, bytes):
                    value = value.decode('utf-8', errors='ignore')
                    if 'UNICODE' in value:
                        prompt_start = value.index('UNICODE') + len('UNICODE\x00\x00')
                        prompt = value[prompt_start:]
                        # カンマ区切りで分割し、改行や余分なスペースを除去
                        prompt_words = [word.strip().replace('\n', ' ').replace('\r', '') for word in prompt.split(',')]
                        # さらにスペースを正規化
                        prompt_words = [' '.join(word.split()) for word in prompt_words if word]
                        print(f"Extracted prompt words: {prompt_words}")
                        for word in prompt_words:
                            for en_word, jp_word in self.word_map.items():
                                if en_word == word:
                                    translated[en_word] = jp_word
                                else:
                                    print(f"No match: '{word}' does not match '{en_word}'")
            
            if not translated:
                filename = os.path.splitext(os.path.basename(image_path))[0].lower()
                print(f"Extracting from filename: {filename}")
                words = filename.split()
                for word in words:
                    for en_word, jp_word in self.word_map.items():
                        if en_word in word:
                            translated[en_word] = jp_word
            
            return translated if translated else {"no_match": "一致なし"}
        except Exception as e:
            print(f"Error parsing metadata for {image_path}: {e}")
            return {"error": str(e)}
