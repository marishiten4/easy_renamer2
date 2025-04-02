import json
import os

class Settings:
    def __init__(self):
        self.config_file = "settings.json"
        self.config = self.load_config()
    
    def load_config(self):
        """設定ファイルを読み込む"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                print(f"Loaded config: {config}")  # デバッグ出力
                return config
        return {"templates": ["カスタム"], "search_words": [], "word_map": {}}
    
    def save_config(self):
        """設定ファイルを保存する"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
        print(f"Saved config: {self.config}")  # デバッグ出力
    
    def get_templates(self):
        """テンプレートを取得する"""
        templates = self.config.get("templates", ["カスタム"])
        print(f"Retrieved templates: {templates}")  # デバッグ出力
        return templates
    
    def set_templates(self, templates):
        """テンプレートを設定する"""
        self.config["templates"] = templates
        print(f"Set templates: {templates}")  # デバッグ出力
    
    def get_search_words(self):
        """検索ワードを取得する"""
        return self.config.get("search_words", [])
    
    def set_search_words(self, words):
        """検索ワードを設定する"""
        self.config["search_words"] = words
    
    def get_word_map(self):
        """ワードマップを取得する"""
        return self.config.get("word_map", {})
    
    def set_word_map(self, word_map):
        """ワードマップを設定する"""
        self.config["word_map"] = word_map
    
    def save(self):
        """設定を保存する（互換性のために残す）"""
        self.save_config()