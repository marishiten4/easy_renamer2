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
            # メタデータの解析（特にexif内のプロンプト）
            for key, value in metadata.items():
                if key == 'exif' and isinstance(value, bytes):
                    # exifデータを文字列に変換
                    value = value.decode('utf-8', errors='ignore')
                    # UNICODE以降のプロンプト部分を抽出
                    if 'UNICODE' in value:
                        prompt_start = value.index('UNICODE') + len('UNICODE\x00\x00')
                        prompt = value[prompt_start:]
                        # カンマ区切りでプロンプトを分割
                        prompt_words = [word.strip() for word in prompt.split(',')]
                        print(f"Extracted prompt words: {prompt_words}")
                        # word_mapと一致するかチェック
                        for word in prompt_words:
                            for en_word, jp_word in self.word_map.items():
                                if en_word == word:
                                    translated[en_word] = jp_word
            
            # メタデータが空の場合、ファイル名から推測
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
