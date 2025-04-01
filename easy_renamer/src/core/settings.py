import json
import os

class Settings:
    def __init__(self):
        self.config_file = "settings.json"
        self.default_word_map = {
            "short hair": "短髪",
            "blue eyes": "青い目",
            "long hair": "長髪"
        }
    
    def load_word_map(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f).get("word_map", self.default_word_map)
        return self.default_word_map
    
    def save_word_map(self, word_map):
        config = {"word_map": word_map}
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
