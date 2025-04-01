from PIL import Image
import piexif
import os

def extract_metadata(image_path):
    """
    Extract metadata from an image file
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing metadata information
    """
    try:
        img = Image.open(image_path)
        metadata = {}
        
        # Extract basic image information
        metadata['format'] = img.format
        metadata['size'] = img.size
        metadata['mode'] = img.mode
        
        # Extract Exif data if available
        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])
            
            # Process Exif data
            if piexif.ExifIFD.UserComment in exif_dict["Exif"]:
                user_comment = exif_dict["Exif"][piexif.ExifIFD.UserComment]
                if user_comment.startswith(b'UNICODE\0'):
                    metadata['user_comment'] = user_comment[8:].decode('utf-16be', errors='ignore')
                else:
                    metadata['user_comment'] = user_comment.decode('utf-8', errors='ignore')
            
            # Extract other useful Exif data
            if '0th' in exif_dict and piexif.ImageIFD.Software in exif_dict['0th']:
                software = exif_dict['0th'][piexif.ImageIFD.Software]
                if isinstance(software, bytes):
                    metadata['software'] = software.decode('utf-8', errors='ignore')
                else:
                    metadata['software'] = software
            
            # Add date time if available
            if '0th' in exif_dict and piexif.ImageIFD.DateTime in exif_dict['0th']:
                date_time = exif_dict['0th'][piexif.ImageIFD.DateTime]
                if isinstance(date_time, bytes):
                    metadata['date_time'] = date_time.decode('utf-8', errors='ignore')
                else:
                    metadata['date_time'] = date_time
        
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {'error': str(e)}

def get_stable_diffusion_prompt(metadata):
    """
    Extract Stable Diffusion prompt from metadata if available
    
    Args:
        metadata: Dictionary containing metadata information
        
    Returns:
        Prompt string or None if not found
    """
    # Check if user comment exists
    if 'user_comment' in metadata:
        # Common format for Stable Diffusion is "positive prompt: ... negative prompt: ..."
        comment = metadata['user_comment'].lower()
        if 'positive prompt:' in comment or 'prompt:' in comment:
            return metadata['user_comment']
    
    # Check if software field indicates Stable Diffusion
    if 'software' in metadata and 'stable diffusion' in metadata['software'].lower():
        return metadata.get('user_comment')
    
    return None

def parse_prompt_keywords(prompt, keyword_list):
    """
    Parse prompt text for relevant keywords
    
    Args:
        prompt: Prompt text
        keyword_list: List of keywords to search for
        
    Returns:
        List of found keywords
    """
    if not prompt or not keyword_list:
        return []
    
    prompt_lower = prompt.lower()
    found_keywords = []
    
    for keyword in keyword_list:
        if keyword.lower() in prompt_lower:
            found_keywords.append(keyword)
    
    return found_keywords
