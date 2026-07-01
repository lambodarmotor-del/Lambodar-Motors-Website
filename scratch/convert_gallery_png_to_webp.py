import os
import re
from PIL import Image

def convert_png_to_webp():
    gallery_dir = r"c:\Users\Harshil\OneDrive\Desktop\website\assets\images\gallery"
    html_root = r"c:\Users\Harshil\OneDrive\Desktop\website"
    
    # 1. Convert PNG files to WEBP in assets/images/gallery/
    converted_files = {}
    png_files = [f for f in os.listdir(gallery_dir) if f.lower().endswith('.png')]
    
    print(f"Found {len(png_files)} PNG files to convert in gallery.")
    
    for filename in png_files:
        png_path = os.path.join(gallery_dir, filename)
        base_name = os.path.splitext(filename)[0]
        webp_filename = base_name + '.webp'
        webp_path = os.path.join(gallery_dir, webp_filename)
        
        # Convert using Pillow
        try:
            with Image.open(png_path) as img:
                # Save as webp with high compression and good quality
                img.save(webp_path, 'WEBP', quality=85)
            print(f"Converted: {filename} -> {webp_filename}")
            converted_files[filename] = webp_filename
            
            # Delete original PNG
            os.remove(png_path)
            print(f"Deleted original: {filename}")
        except Exception as e:
            print(f"Error converting {filename}: {e}")
            
    if not converted_files:
        print("No files converted.")
        return
        
    # 2. Search and replace references in all HTML files
    print("\nScanning HTML files for image references...")
    html_files = []
    for root, dirs, files in os.walk(html_root):
        if '.git' in root or '.backup_rollback' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    updated_files_count = 0
    
    for html_path in html_files:
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        modified = False
        
        # Search for any references to the converted gallery PNGs and replace with webp
        for png_name, webp_name in converted_files.items():
            pattern = re.escape(png_name)
            if re.search(pattern, content):
                content = re.sub(pattern, webp_name, content)
                modified = True
                print(f"  Updated reference '{png_name}' -> '{webp_name}' in {html_path}")
                
        if modified:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_files_count += 1
            
    print(f"\nCompleted! Converted {len(converted_files)} images to WEBP, and updated references in {updated_files_count} HTML files.")

if __name__ == '__main__':
    convert_png_to_webp()
