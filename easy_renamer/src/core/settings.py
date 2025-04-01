import os
import json
from pathlib import Path

class Settings:
    def __init__(self, app_name="EasyRenamer"):
        """Initialize Settings manager
        
        Args:
            app_name: Application name for settings directory
        """
        self.app_name = app_name
        self.settings_dir = self._get_settings_dir()
        self.settings_file = os.path.join(self.settings_dir, 'settings.json')
        
        # Create directory if it doesn't exist
        os.makedirs(self.settings_dir, exist_ok=True)
        
        # Load or create settings
        self.settings = self._load_settings()
    
    def _get_settings_dir(self):
        """Get platform-specific settings directory"""
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('APPDATA')
            return os.path.join(app_data, self.app_name)
        else:  # macOS/Linux
            home = os.path.expanduser("~")
            return os.path.join(home, f".{self.app_name.lower()}")
    
    def _load_settings(self):
        """Load settings from file or create default"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._create_default_settings()
        else:
            return self._create_default_settings()
    
    def _create_default_settings(self):
        """Create default settings structure"""
        settings = {
            'template_texts': [
                "新品 ①~③枚目実際のお品 これらの画像加工なし 撮影現物発送 写真追加等承りますのでコメント下さい",
                "作成 画像なし 撮影現物発送",
                "作成 ①~③枚目実際のお品 他イメージ"
            ],
            'big_words': [
                "イラスト", "アート", "絵画", "風景画", "肖像画", "アニメ", "漫画", 
                "キャラクター", "ポートレート", "美少女", "美人", "動物", "風景"
            ],
            'small_words': [
                "かわいい", "美しい", "綺麗", "素敵", "おしゃれ", "シンプル", "豪華", 
                "高級感", "レトロ", "モダン", "ポップ", "クール", "シック"
            ],
            'metadata_keywords': [
                "girl", "boy", "woman", "man", "landscape", 
                "portrait", "anime", "manga", "character", "nature", 
                "cat", "dog", "1girl", "2girls"
            ],
            'keyword_mappings': {
                "1girl": ["少女", "女の子", "女子", "一人娘"],
                "2girls": ["少女たち", "女の子たち", "女子たち", "二人娘"],
                "girl": ["少女", "女の子", "女子"],
                "boy": ["少年", "男の子", "男子"],
                "woman": ["女性", "女", "レディ"],
                "man": ["男性", "男", "紳士"],
                "landscape": ["風景", "景色", "シーン"],
                "portrait": ["肖像", "ポートレート"],
                "anime": ["アニメ", "アニメーション"],
                "manga": ["漫画", "コミック"],
                "character": ["キャラクター", "キャラ"],
                "nature": ["自然", "ネイチャー"],
                "cat": ["猫", "ねこ", "ネコ"],
                "dog": ["犬", "いぬ", "イヌ"]
            },
            'ui': {
                'last_folder': '',
                'window_size': [1000, 700],
                'number_position': 'suffix',
                'custom_numbering': '{n:02d}'
            }
        }
        
        # Save default settings
        self.save_settings(settings)
        
        return settings
    
    def save_settings(self, settings=None):
        """Save settings to file
        
        Args:
            settings: Settings dictionary to save (uses self.settings if None)
        """
        if settings is None:
            settings = self.settings
        
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        # Update current settings
        self.settings = settings
    
    def get_setting(self, key, default=None):
        """Get a setting value by key
        
        Args:
            key: Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        keys = key.split('.')
        value = self.settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, key, value):
        """Set a setting value by key
        
        Args:
            key: Setting key (supports dot notation for nested keys)
            value: Value to set
            
        Returns:
            Success status
        """
        keys = key.split('.')
        settings = self.settings
        
        # Navigate to the nested dictionary
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        # Set the value
        settings[keys[-1]] = value
        
        # Save the updated settings
        self.save_settings()
        return True
    
    def add_to_list(self, list_key, value):
        """Add a value to a list setting
        
        Args:
            list_key: Key for the list setting
            value: Value to add
            
        Returns:
            Success status
        """
        if value:
            current_list = self.get_setting(list_key, [])
            if value not in current_list:
                current_list.append(value)
                self.set_setting(list_key, current_list)
                return True
        return False
    
    def remove_from_list(self, list_key, index):
        """Remove an item from a list setting by index
        
        Args:
            list_key: Key for the list setting
            index: Index to remove
            
        Returns:
            Success status
        """
        current_list = self.get_setting(list_key, [])
        try:
            current_list.pop(index)
            self.set_setting(list_key, current_list)
            return True
        except (IndexError, TypeError):
            return False
