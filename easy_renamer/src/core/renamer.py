import os
import json
import shutil
from pathlib import Path
from PIL import Image
import piexif
from datetime import datetime

class EasyRenamer:
    def __init__(self):
        """Initialize the EasyRenamer with settings"""
        self.settings_file = os.path.join(self.get_app_data_dir(), 'settings.json')
        self.renamed_dir = os.path.join(self.get_app_data_dir(), 'renamed_images')
        
        # Ensure directories exist
        os.makedirs(self.get_app_data_dir(), exist_ok=True)
        os.makedirs(self.renamed_dir, exist_ok=True)
        
        # Load or create settings
        self.load_settings()
    
    def get_app_data_dir(self):
        """Get application data directory based on platform"""
        app_name = "EasyRenamer"
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('APPDATA')
            return os.path.join(app_data, app_name)
        else:  # macOS/Linux
            home = os.path.expanduser("~")
            return os.path.join(home, f".{app_name.lower()}")
    
    def load_settings(self):
        """Load settings from file or create default"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except:
                self.create_default_settings()
        else:
            self.create_default_settings()
    
    def create_default_settings(self):
        """Create default settings"""
        self.settings = {
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
            }
        }
        self.save_settings()
    
    def save_settings(self):
        """Save settings to file"""
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)
    
    def add_word(self, category, word):
        """Add a word to a category"""
        if word and word not in self.settings[category]:
            self.settings[category].append(word)
            self.save_settings()
            return True
        return False
    
    def remove_word(self, category, index):
        """Remove a word from a category by index"""
        try:
            self.settings[category].pop(index)
            self.save_settings()
            return True
        except:
            return False
    
    def add_keyword_mapping(self, keyword, mapped_values):
        """Add a keyword mapping"""
        if not keyword:
            return False
            
        # Split mapped values by comma and strip whitespace
        mapped_list = [x.strip() for x in mapped_values.split(',') if x.strip()]
        
        if mapped_list:
            self.settings['keyword_mappings'][keyword] = mapped_list
            self.save_settings()
            return True
        return False
    
    def remove_keyword_mapping(self, keyword):
        """Remove a keyword mapping"""
        if keyword in self.settings['keyword_mappings']:
            del self.settings['keyword_mappings'][keyword]
            self.save_settings()
            return True
        return False
    
    def extract_metadata_keywords(self, image_file):
        """Extract keywords from image metadata"""
        try:
            # Either a file path or a file-like object
            if isinstance(image_file, str):
                img = Image.open(image_file)
            else:
                img = Image.open(image_file)
                image_file.seek(0)  # Reset file pointer
            
            result = {"extracted": [], "mapped": []}
            
            # Try to get Exif data
            if "exif" in img.info:
                exif_dict = piexif.load(img.info["exif"])
                
                # Check UserComment in Exif
                if piexif.ExifIFD.UserComment in exif_dict["Exif"]:
                    user_comment = exif_dict["Exif"][piexif.ExifIFD.UserComment]
                    if user_comment.startswith(b'UNICODE\0'):
                        comment_text = user_comment[8:].decode('utf-16be', errors='ignore')
                    else:
                        comment_text = user_comment.decode('utf-8', errors='ignore')
                    
                    # Parse extracted text
                    result["extracted"] = self._parse_metadata_text(comment_text)
                    result["mapped"] = self._map_keywords(result["extracted"])
            
            # If no metadata found, try to check filename for basic keywords
            if not result["extracted"] and isinstance(image_file, str):
                base_name = os.path.basename(image_file).lower()
                keywords = self.settings['metadata_keywords']
                found_keywords = [kw for kw in keywords if kw.lower() in base_name]
                if found_keywords:
                    result["extracted"] = found_keywords
                    result["mapped"] = self._map_keywords(found_keywords)
                    
            return result
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {"extracted": [], "mapped": []}
    
    def _parse_metadata_text(self, text):
        """Parse metadata text to extract relevant keywords"""
        # Simple parsing for now - look for keywords in the text
        keywords = self.settings['metadata_keywords']
        found_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in text.lower():
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _map_keywords(self, keywords):
        """Map extracted keywords to configured mapped values"""
        mapped_words = []
        for keyword in keywords:
            if keyword in self.settings['keyword_mappings']:
                mapped_words.extend(self.settings['keyword_mappings'][keyword])
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(mapped_words))
    
    def rename_files(self, files, base_name, numbering_format="{n:02d}", position="suffix", output_dir=None):
        """Rename files with numbering
        
        Args:
            files: List of file paths
            base_name: Base name for files
            numbering_format: Format for numbering
            position: Position of number ('prefix' or 'suffix')
            output_dir: Optional output directory
            
        Returns:
            Dictionary mapping original filenames to new filenames
        """
        if output_dir is None:
            output_dir = self.renamed_dir
        else:
            output_dir = os.path.abspath(output_dir)
            
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Clear any existing files in the output directory
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        result = {}
        for i, file_path in enumerate(files, 1):
            # Handle both file paths and file objects
            if isinstance(file_path, str):
                original_filename = os.path.basename(file_path)
                file_ext = os.path.splitext(original_filename)[1]
            else:
                original_filename = file_path.name
                file_ext = os.path.splitext(original_filename)[1]
            
            # Format the number according to the specified format
            try:
                number_str = numbering_format.format(n=i)
            except:
                number_str = str(i)  # Fallback if format fails
            
            # Create new filename based on position preference
            if position == "prefix":
                new_filename = f"{number_str}_{base_name}{file_ext}"
            else:  # suffix
                new_filename = f"{base_name}_{number_str}{file_ext}"
            
            # Create output path
            output_path = os.path.join(output_dir, new_filename)
            
            # Copy or save the file
            try:
                if isinstance(file_path, str):
                    shutil.copy2(file_path, output_path)
                else:
                    with open(output_path, 'wb') as out_file:
                        file_path.seek(0)  # Reset file pointer
                        out_file.write(file_path.read())
                
                result[original_filename] = new_filename
            except Exception as e:
                print(f"Error copying file {original_filename}: {e}")
        
        return result
    
    def create_zip_archive(self, source_dir=None, output_path=None):
        """Create a ZIP archive of renamed files
        
        Args:
            source_dir: Source directory (defaults to renamed_images)
            output_path: Output path for ZIP file
            
        Returns:
            Path to the created ZIP file
        """
        if source_dir is None:
            source_dir = self.renamed_dir
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.get_app_data_dir(), f"renamed_images_{timestamp}.zip")
        
        # Create ZIP file
        shutil.make_archive(
            os.path.splitext(output_path)[0],  # Remove .zip extension if present
            'zip',
            source_dir
        )
        
        return output_path
