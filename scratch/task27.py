import os
import re

def add_breadcrumbs():
    html_files = []
    # Walk and collect all HTML files except index.html and task/temp files
    for root, dirs, files in os.walk("."):
        parts = root.split(os.sep)
        if any(p.startswith('.') and p not in ['.', '..'] for p in parts):
            continue
        for file in files:
            if file.endswith(".html") and file != "index.html" and not file.startswith("temp"):
                html_files.append(os.path.join(root, file))

    updated_files = []
    for filepath in html_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()

        # If breadcrumb already exists, skip
        if 'class="breadcrumb-nav"' in content or "breadcrumb-nav" in content:
            print(f"Breadcrumb already exists in {filepath}, skipping.")
            continue

        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if not title_match:
            print(f"Warning: No title tag found in {filepath}, skipping.")
            continue
            
        full_title = title_match.group(1).strip()
        # Clean title to get page name
        # Split by | or - or —
        page_name = full_title
        for delimiter in ['|', '-', '—']:
            if delimiter in page_name:
                page_name = page_name.split(delimiter)[0].strip()
                
        # Specialized page name overrides if needed
        if "AC Service" in page_name:
            page_name = "AC Service"
        elif "About" in page_name:
            page_name = "About"
        elif "FAQ" in page_name:
            page_name = "FAQ"
        elif "Pricing" in page_name:
            page_name = "Pricing"
        elif "Insurance Claim" in page_name:
            page_name = "Insurance Claim"
        elif "Denting" in page_name:
            page_name = "Denting & Painting"
        elif "Battery" in page_name:
            page_name = "Battery, Brakes & Oil"
        elif "Detailing" in page_name:
            page_name = "Car Detailing"
        elif "Engine" in page_name:
            page_name = "Engine Service"
        elif "Page Not Found" in page_name or "404" in page_name:
            page_name = "Page Not Found"

        # Construct breadcrumb HTML
        breadcrumb_html = f"""
  <nav aria-label="Breadcrumb" class="breadcrumb-nav">
    <ol class="breadcrumb-list">
      <li><a href="/">Home</a></li>
      <li>{page_name}</li>
    </ol>
  </nav>"""

        # We want to insert this immediately inside the first <div class="section-container"...>
        # Let's search for first section-container
        pattern = r'(<div class="section-container"[^>]*>)'
        match = re.search(pattern, content)
        
        if match:
            # Insert after the matched tag
            tag = match.group(1)
            new_tag = tag + breadcrumb_html
            new_content = content.replace(tag, new_tag, 1)
        elif "error-container" in content:
            # Fallback for 404.html
            tag_pattern = r'(<div class="error-container"[^>]*>)'
            err_match = re.search(tag_pattern, content)
            if err_match:
                tag = err_match.group(1)
                new_tag = tag + breadcrumb_html
                new_content = content.replace(tag, new_tag, 1)
            else:
                print(f"Warning: Could not find container in {filepath}, skipping.")
                continue
        else:
            print(f"Warning: Could not find section-container in {filepath}, skipping.")
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_files.append(filepath)
        print(f"Added breadcrumbs with page name '{page_name}' to {filepath}")

    print(f"Total files updated: {len(updated_files)}")

if __name__ == "__main__":
    add_breadcrumbs()
