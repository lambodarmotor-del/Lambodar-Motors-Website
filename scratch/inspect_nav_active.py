import os
import re

def inspect_nav_active():
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Exclude directories
        if '.git' in root or '.backup_rollback' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files to inspect.")
    
    nav_pattern = re.compile(r'<nav class="nav-menu">(.*?)</nav>', re.DOTALL)
    mobile_nav_pattern = re.compile(r'<nav class="mobile-nav-links">(.*?)</nav>', re.DOTALL)
    
    for path in html_files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        nav_match = nav_pattern.search(content)
        mobile_match = mobile_nav_pattern.search(content)
        
        print(f"\n--- {path} ---")
        if nav_match:
            print("Desktop Nav Links:")
            links = re.findall(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>|<a\s+[^>]*class="([^"]+)"[^>]*href="([^"]+)"[^>]*>(.*?)</a>|<a\s+[^>]*href="([^"]+)"[^>]*class="([^"]+)"[^>]*>(.*?)</a>', nav_match.group(1))
            # Let's just find all <a> tags inside the nav match
            a_tags = re.findall(r'<a\s+[^>]*>.*?</a>', nav_match.group(1))
            for tag in a_tags:
                if 'active' in tag:
                    print(f"  [ACTIVE] {tag.strip()}")
                else:
                    print(f"           {tag.strip()}")
        else:
            print("Desktop Nav: NOT FOUND")
            
        if mobile_match:
            print("Mobile Nav Links:")
            a_tags = re.findall(r'<a\s+[^>]*>.*?</a>', mobile_match.group(1))
            for tag in a_tags:
                if 'active' in tag:
                    print(f"  [ACTIVE] {tag.strip()}")
                else:
                    print(f"           {tag.strip()}")
        else:
            print("Mobile Nav: NOT FOUND")

if __name__ == '__main__':
    inspect_nav_active()
