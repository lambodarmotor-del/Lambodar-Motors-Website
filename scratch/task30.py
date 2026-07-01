import os
import re

def replace_auto_repair_schema():
    html_files = []
    # Walk and collect all HTML files except index.html and task/temp files
    for root, dirs, files in os.walk("."):
        parts = root.split(os.sep)
        if any(p.startswith('.') and p not in ['.', '..'] for p in parts) or "backup" in root:
            continue
        for file in files:
            if file.endswith(".html") and file != "index.html" and not file.startswith("temp"):
                html_files.append(os.path.join(root, file))

    updated_count = 0
    for filepath in html_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()

        # If it doesn't contain AutoRepair, skip
        if '"AutoRepair"' not in content and "'AutoRepair'" not in content:
            continue

        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if not title_match:
            continue
            
        full_title = title_match.group(1).strip()
        # Clean title to get page name
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

        # Format filename relative to root (with forward slashes)
        rel_path = os.path.relpath(filepath, ".").replace("\\", "/")
        if rel_path.startswith("./"):
            rel_path = rel_path[2:]

        # Construct BreadcrumbList schema HTML
        breadcrumb_schema_html = f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [{{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://lambodar-motors.vercel.app/"
    }},{{
      "@type": "ListItem",
      "position": 2,
      "name": "{page_name}",
      "item": "https://lambodar-motors.vercel.app/{rel_path}"
    }}]
  }}
  </script>"""

        # Regex to find <script type="application/ld+json">...</script> block that contains AutoRepair
        # We use re.DOTALL to match multiline
        pattern = r'<script\s+type="application/ld\+json">[^<]*?"AutoRepair"[^<]*?</script>'
        content_new, count = re.subn(pattern, breadcrumb_schema_html, content, flags=re.DOTALL)

        if count > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_new)
            updated_count += 1
            print(f"Replaced AutoRepair schema with BreadcrumbList schema in {filepath}")
        else:
            print(f"Warning: Regex did not match AutoRepair schema in {filepath}")

    print(f"Total files updated: {updated_count}")

if __name__ == "__main__":
    replace_auto_repair_schema()
