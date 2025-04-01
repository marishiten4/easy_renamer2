import os
import sys
import tempfile
import re
import shutil
from PIL import Image, ImageQt
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon, QImage

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_thumbnail(image_path, max_size=(200, 200)):
    """Create a thumbnail from an image file
    
    Args:
        image_path: Path to image file
        max_size: Maximum size for thumbnail (width, height)
        
    Returns:
        QPixmap object with the thumbnail
    """
    try:
        # Open image
        pil_img = Image.open(image_path)
        
        # Create thumbnail
        pil_img.thumbnail(max_size, Image.LANCZOS)
        
        # Convert PIL Image to QPixmap via QImage
        if pil_img.mode != "RGBA":
            pil_img = pil_img.convert("RGBA")
        
        data = pil_img.tobytes("raw", "RGBA")
        qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format_RGBA8888)
        
        pixmap = QPixmap.fromImage(qimage)
        return pixmap
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return QPixmap()

def validate_filename(filename):
    """Validate filename for Windows, macOS, and Linux
    
    Args:
        filename: Filename to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Check length (Windows has a 255 character limit)
    if len(filename) > 255:
        return False
    
    # Check invalid characters
    invalid_chars = r'[\\/:*?"<>|]'
    if re.search(invalid_chars, filename):
        return False
    
    # Check reserved names on Windows
    if os.name == 'nt':
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                         'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
                         'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        
        name_without_ext = os.path.splitext(filename)[0].upper()
        if name_without_ext in reserved_names:
            return False
    
    return True

def count_characters(text):
    """Count characters considering Japanese characters as 2 bytes
    
    Args:
        text: Text to count characters
        
    Returns:
        Character count
    """
    count = 0
    for char in text:
        # Japanese characters (hiragana, katakana, kanji) are counted as 2
        if ord(char) > 127:
            count += 2
        else:
            count += 1
    return count

def create_zip_from_folder(source_folder, output_zip):
    """Create a zip file from a folder
    
    Args:
        source_folder: Source folder path
        output_zip: Output zip file path
        
    Returns:
        Output zip file path
    """
    # Remove .zip extension if present to avoid double extension
    base_output = os.path.splitext(output_zip)[0]
    
    # Create zip archive
    shutil.make_archive(base_output, 'zip', source_folder)
    
    # Return path with .zip extension
    return f"{base_output}.zip"

def format_byte_size(size_bytes):
    """Format byte size to human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
