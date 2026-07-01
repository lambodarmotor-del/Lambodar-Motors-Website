import os
import glob
import shutil
import sys

def copy_image(idx):
    target_dir = r'c:\Users\Harshil\OneDrive\Desktop\website\assets\images\blog'
    
    # Locate files matching the pattern in all brain subdirectories
    pattern = r'C:\Users\Harshil\.gemini\antigravity\brain\*\blog_post_unique_{}_*.png'.format(idx)
    files = glob.glob(pattern)
    
    if not files:
        print(f"Error: No generated image files found matching index {idx} in any brain directory")
        return False
        
    # Get the newest matching file
    newest = max(files, key=os.path.getmtime)
    dest = os.path.join(target_dir, f'blog_post_unique_{idx}.png')
    
    # Copy file
    try:
        shutil.copy(newest, dest)
        print(f"Success: Copied {os.path.basename(newest)} to {dest}")
        return True
    except Exception as e:
        print(f"Error during copy of index {idx}: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: py copy_image.py <index>")
        sys.exit(1)
    try:
        idx = int(sys.argv[1])
        success = copy_image(idx)
        if not success:
            sys.exit(1)
    except ValueError:
        print("Error: Index must be an integer.")
        sys.exit(1)
