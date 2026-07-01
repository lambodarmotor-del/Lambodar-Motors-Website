import os

def add_back_to_top_button():
    html_files = []
    for root, dirs, files in os.walk("."):
        parts = root.split(os.sep)
        if any(p.startswith('.') and p not in ['.', '..'] for p in parts):
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

        if 'class="back-to-top"' in content or "back-to-top" in content:
            print(f"Back-to-top button already exists in {filepath}, skipping.")
            continue

        if "</body>" in content:
            button_html = '  <button class="back-to-top" aria-label="Back to top">↑</button>\n</body>'
            content = content.replace("</body>", button_html, 1)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            updated_count += 1
            print(f"Added back-to-top button to {filepath}")
        else:
            print(f"Warning: No </body> tag found in {filepath}")

    print(f"Total files updated: {updated_count}")

if __name__ == "__main__":
    add_back_to_top_button()
