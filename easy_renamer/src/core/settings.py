import json
import os

class Settings:
    def __init__(self):
        self.config_file = "settings.json"
        self.default_config = {
            "templates": ["出品用_キャラ", "テスト_画像", "カスタム"],
            "search_words": ["short", "long", "blue"],
            "word_map": {"short hair": "短髪", "blue eyes": "青い目", "long hair": "長髪"}
        }
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.default_config
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_templates(self):
        return self.config["templates"]
    
    def get_search_words(self):
        return self.config["search_words"]
    
    def get_word_map(self):
        return self.config["word_map"]
