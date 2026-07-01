import os

def replace_og_image():
    html_files = []
    for root, dirs, files in os.walk("."):
        # Ignore backup folder
        parts = root.split(os.sep)
        if any(p.startswith('.') and p not in ['.', '..'] for p in parts) or "backup" in root:
            continue
        for file in files:
            if file.endswith(".html") and not file.startswith("temp"):
                html_files.append(os.path.join(root, file))

    updated_count = 0
    for filepath in html_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()

        original_content = content
        # Replace case-insensitively and handle whitespace / slash styles
        content = content.replace("assets/images/logo/og-image.svg", "assets/images/logo/og-image.png")
        
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            updated_count += 1
            print(f"Updated og:image reference in {filepath}")

    print(f"Total files updated: {updated_count}")

if __name__ == "__main__":
    replace_og_image()
