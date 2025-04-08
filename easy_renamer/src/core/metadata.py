from PIL import Image
import os
import unicodedata
from core.settings import Settings

class MetadataParser:
    def __init__(self):
        self.settings = Settings()
        self.word_map = self.settings.get_word_map()
    
    def update_word_map(self):
        """設定変更後にword_mapを更新"""
        self.word_map = self.settings.get_word_map()
        print(f"Updated word_map: {self.word_map}")
    
    def normalize_string(self, s):
        """文字列を正規化（ユニコード正規化＋不可視文字除去＋スペース正規化）"""
        # NULL文字（\x00）を除去
        s = s.replace('\x00', '')
        # ユニコード正規化（NFC形式）
        s = unicodedata.normalize('NFC', s)
        # 不可視文字や制御文字を除去
        s = ''.join(c for c in s if unicodedata.category(c) not in ('Cc', 'Cf'))
        # スペースを正規化
        s = ' '.join(s.split())
        return s.strip()

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
                        # さらに正規化
                        prompt_words = [self.normalize_string(word) for word in prompt_words if word]
                        print(f"Extracted prompt words: {prompt_words}")
                        for word in prompt_words:
                            for en_word, jp_word in self.word_map.items():
                                normalized_en_word = self.normalize_string(en_word)
                                if normalized_en_word == word:
                                    translated[en_word] = jp_word
                                else:
                                    print(f"No match: '{word}' ({repr(word)}) does not match '{normalized_en_word}' ({repr(normalized_en_word)})")
            
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