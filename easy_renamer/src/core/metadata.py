import exifread
from PIL import Image

class MetadataParser:
    def parse(self, image_path):
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
        metadata = {tag: str(tags[tag]) for tag in tags}
        return metadata  # 例: {"ImageDescription": "short hair, blue eyes"}
