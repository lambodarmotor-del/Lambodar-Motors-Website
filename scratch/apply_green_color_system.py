import os
import re

def update_css_and_html():
    workspace = r"c:\Users\Harshil\OneDrive\Desktop\website"
    css_path = os.path.join(workspace, 'assets', 'css', 'style.css')
    
    # 1. Update style.css
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
        
    # We will update .btn-whatsapp and .btn-whatsapp:hover
    css_content = re.sub(
        r'\.btn-whatsapp\s*\{([^}]+)\}',
        r'.btn-whatsapp {\n  background: #25D366; /* Exact WhatsApp Green */\n  color: #132920; /* Dark forest green for softer contrast and high readability */\n  font-weight: 700;\n  box-shadow: 0 4px 14px rgba(37, 211, 102, 0.2);\n}',
        css_content
    )
    
    css_content = re.sub(
        r'\.btn-whatsapp:hover\s*\{([^}]+)\}',
        r'.btn-whatsapp:hover {\n  background: #20ba59;\n  color: #0d1e16;\n  box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);\n  transform: translateY(-2px);\n}',
        css_content
    )
    
    # Update slider-label-after colors
    css_content = re.sub(
        r'\.slider-label-after\s*\{([^}]+)\}',
        r'.slider-label-after {\n  right: 20px;\n  background: #09090b;\n  border-color: #25D366;\n  color: #25D366;\n}',
        css_content
    )
    
    # Append floating-whatsapp, mobile-cta-whatsapp, mobile-cta-call classes at the end of style.css if not already present
    extra_css = """
/* Centrally Managed Floating & Sticky Mobile CTA Styles */
.floating-whatsapp {
  position: fixed;
  bottom: 80px;
  right: 20px;
  z-index: 999;
  background: #25D366;
  color: #132920; /* Dark forest green icon */
  border-radius: 50%;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
  text-decoration: none;
  transition: all 0.3s ease;
}

.floating-whatsapp:hover {
  background: #20ba59;
  color: #0d1e16;
  transform: scale(1.08);
  box-shadow: 0 6px 20px rgba(37, 211, 102, 0.5);
}

.mobile-cta-whatsapp {
  display: inline-flex;
  width: 50%;
  padding: 14px;
  background: #25D366;
  color: #132920; /* Dark forest green text */
  text-align: center;
  font-weight: 700;
  text-decoration: none;
  justify-content: center;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.mobile-cta-whatsapp:hover {
  background: #20ba59;
  color: #0d1e16;
}

.mobile-cta-call {
  display: inline-flex;
  width: 50%;
  padding: 14px;
  background: #2563eb;
  color: #ffffff;
  text-align: center;
  font-weight: 700;
  text-decoration: none;
  justify-content: center;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.mobile-cta-call:hover {
  background: #1d4ed8;
}
"""
    if '.floating-whatsapp' not in css_content:
        css_content += extra_css
        
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("Updated assets/css/style.css successfully.")
    
    # 2. Update HTML Files
    html_files = []
    for root, dirs, files in os.walk(workspace):
        if '.git' in root or '.backup_rollback' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Scanning and updating {len(html_files)} HTML files...")
    
    # Patterns to match and replace
    # Pattern A: Floating WhatsApp inline style
    floating_style_pattern = re.compile(
        r'style="position:\s*fixed;\s*bottom:\s*80px;\s*right:\s*20px;\s*z-index:\s*999;\s*background:\s*#25D366;\s*color:\s*#fff;\s*border-radius:\s*50%;\s*width:\s*56px;\s*height:\s*56px;\s*display:\s*flex;\s*align-items:\s*center;\s*justify-content:\s*center;\s*box-shadow:\s*0\s*4px\s*12px\s*rgba\(0,\s*0,\s*0,\s*0\.3\);\s*text-decoration:\s*none;\s*transition:\s*all\s*0\.3s\s*ease;"',
        re.IGNORECASE
    )
    
    # Pattern B: Sticky Mobile CTA Call inline style
    call_style_pattern = re.compile(
        r'style="display:\s*inline-flex;\s*width:\s*50%;\s*padding:\s*14px;\s*background:\s*#2563eb;\s*color:\s*#fff;\s*text-align:\s*center;\s*font-weight:\s*600;\s*text-decoration:\s*none;\s*justify-content:\s*center;\s*align-items:\s*center;\s*gap:\s*6px;"',
        re.IGNORECASE
    )
    
    # Pattern C: Sticky Mobile CTA WhatsApp inline style
    whatsapp_style_pattern = re.compile(
        r'style="display:\s*inline-flex;\s*width:\s*50%;\s*padding:\s*14px;\s*background:\s*#25D366;\s*color:\s*#fff;\s*text-align:\s*center;\s*font-weight:\s*600;\s*text-decoration:\s*none;\s*justify-content:\s*center;\s*align-items:\s*center;\s*gap:\s*6px;"',
        re.IGNORECASE
    )
    
    updated_html_count = 0
    for path in html_files:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        modified = False
        
        # Replace Floating button style with class
        if floating_style_pattern.search(content):
            content = floating_style_pattern.sub('class="floating-whatsapp"', content)
            modified = True
            
        # Replace Mobile Call button style with class
        if call_style_pattern.search(content):
            content = call_style_pattern.sub('class="mobile-cta-call"', content)
            modified = True
            
        # Replace Mobile WhatsApp button style with class
        if whatsapp_style_pattern.search(content):
            content = whatsapp_style_pattern.sub('class="mobile-cta-whatsapp"', content)
            modified = True
            
        # For index.html, update the inline style color of the direct WhatsApp button we added
        if 'index.html' in path:
            direct_wa_pattern = r'class="btn btn-whatsapp"\s*style="([^"]*)"'
            if re.search(direct_wa_pattern, content):
                # Update text color from white (none specified or inherit) to #132920 inside the inline style
                # Actually, our class btn-whatsapp already defines color: #132920, so we can just remove the style entirely or clean it up
                # Let's clean it up by replacing the style attribute or removing it, but wait, it has padding, flex, etc.
                # Let's just append color: #132920; to its inline style to be absolutely certain
                content = re.sub(
                    r'(class="btn btn-whatsapp"\s*style=")([^"]*)(")',
                    r'\1color: #132920; \2\3',
                    content
                )
                modified = True
                
        if modified:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_html_count += 1
            
    print(f"Updated {updated_html_count} HTML files with class-based green button styles.")

if __name__ == '__main__':
    update_css_and_html()
