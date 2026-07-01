import os
import re

def fix_html_navs():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.backup_rollback' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Found {len(html_files)} HTML files to process.")
    
    for path in html_files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # We need to process both:
        # 1. <nav class="nav-menu">...</nav>
        # 2. <nav class="mobile-nav-links">...</nav>
        
        # Helper function to clean a single link tag
        def clean_link(tag):
            # Remove class="active", class='active', active="true", class="active ", class=" active"
            tag = re.sub(r'\s*class=["\']active["\']', '', tag)
            # Handle cases where class has other items, e.g. class="some-class active" or class="active some-class"
            tag = re.sub(r'class=["\']\s*active\s+([^"\']+)["\']', r'class="\1"', tag)
            tag = re.sub(r'class=["\']([^"\']+)\s+active\s*["\']', r'class="\1"', tag)
            # Remove any trailing spaces inside tag before >
            tag = re.sub(r'\s+>', '>', tag)
            return tag
            
        # Helper function to add class="active" to a link tag
        def make_active(tag):
            tag = clean_link(tag)
            # Insert class="active" before href or inside tag
            if 'class=' in tag:
                # Add active class to existing class attribute
                tag = re.sub(r'class=["\']([^"\']+)["\']', r'class="\1 active"', tag)
            else:
                # Add class="active" right after '<a '
                tag = re.sub(r'<a\s+', '<a class="active" ', tag)
            return tag

        def process_nav_section(nav_content, is_mobile, file_name, is_blog):
            # Parse all <a> tags
            a_tags = re.findall(r'<a\s+[^>]*>.*?</a>', nav_content, re.DOTALL)
            new_nav_content = nav_content
            
            for tag in a_tags:
                cleaned = clean_link(tag)
                
                # Check if this tag should be active
                should_be_active = False
                
                # Extract href
                href_match = re.search(r'href=["\']([^"\']+)["\']', tag)
                if href_match:
                    href = href_match.group(1)
                    
                    if file_name == 'about.html':
                        if 'about.html' in href:
                            should_be_active = True
                    elif file_name == 'faq.html':
                        if 'faq.html' in href:
                            should_be_active = True
                    elif is_blog:
                        # Blog subfolder files have href="index.html" or similar for blog.
                        # Wait, a blog link in nav might look like "blog/index.html" (from root) or "index.html" (from inside blog/)
                        # Let's check the href name
                        if href == 'index.html' or href == 'blog/index.html' or href.endswith('/blog/index.html'):
                            should_be_active = True
                    elif file_name == 'index.html':
                        # Homepage desktop nav active on #home
                        if not is_mobile and href == '#home':
                            should_be_active = True
                            
                if should_be_active:
                    replacement = make_active(tag)
                else:
                    replacement = cleaned
                    
                if tag != replacement:
                    new_nav_content = new_nav_content.replace(tag, replacement)
                    
            return new_nav_content

        # Determine file type
        file_name = os.path.basename(path)
        is_blog = 'blog' in path.split(os.sep)
        
        # 1. Desktop Nav
        nav_pattern = re.compile(r'(<nav class="nav-menu">)(.*?)(</nav>)', re.DOTALL)
        nav_match = nav_pattern.search(content)
        if nav_match:
            prefix, nav_inner, suffix = nav_match.groups()
            new_inner = process_nav_section(nav_inner, False, file_name, is_blog)
            if new_inner != nav_inner:
                content = content.replace(prefix + nav_inner + suffix, prefix + new_inner + suffix)
                modified = True
                
        # 2. Mobile Nav
        mobile_nav_pattern = re.compile(r'(<nav class="mobile-nav-links">)(.*?)(</nav>)', re.DOTALL)
        mobile_nav_match = mobile_nav_pattern.search(content)
        if mobile_nav_match:
            prefix, nav_inner, suffix = mobile_nav_match.groups()
            new_inner = process_nav_section(nav_inner, True, file_name, is_blog)
            if new_inner != nav_inner:
                content = content.replace(prefix + nav_inner + suffix, prefix + new_inner + suffix)
                modified = True
                
        if modified:
            print(f"Updated: {path}")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    fix_html_navs()
