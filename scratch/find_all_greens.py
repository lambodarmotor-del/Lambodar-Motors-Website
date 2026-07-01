import os
import re

def parse_color(color_str):
    # Try hex
    hex_match = re.match(r'#([a-fA-F0-9]{3,8})', color_str)
    if hex_match:
        val = hex_match.group(1)
        if len(val) == 3:
            r = int(val[0]*2, 16)
            g = int(val[1]*2, 16)
            b = int(val[2]*2, 16)
        elif len(val) == 6:
            r = int(val[0:2], 16)
            g = int(val[2:4], 16)
            b = int(val[4:6], 16)
        else:
            return None
        return (r, g, b)
    return None

def find_greens():
    html_root = r"c:\Users\Harshil\OneDrive\Desktop\website"
    color_pattern = re.compile(r'#[a-fA-F0-9]{3,6}|rgb\([^)]+\)|hsl\([^)]+\)')
    
    greens = []
    
    # Scan CSS
    css_path = os.path.join(html_root, 'assets', 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                for match in color_pattern.finditer(line):
                    color = match.group(0)
                    parsed = parse_color(color)
                    if parsed:
                        r, g, b = parsed
                        # If green component is dominant and high
                        if g > 150 and g > r * 1.2 and g > b * 1.2:
                            greens.append(('CSS', css_path, idx+1, color, line.strip()))
                            
    # Scan HTML files
    for root, dirs, files in os.walk(html_root):
        if '.git' in root or '.backup_rollback' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for idx, line in enumerate(f):
                        for match in color_pattern.finditer(line):
                            color = match.group(0)
                            parsed = parse_color(color)
                            if parsed:
                                r, g, b = parsed
                                if g > 150 and g > r * 1.2 and g > b * 1.2:
                                    greens.append(('HTML', path, idx+1, color, line.strip()))
                                    
    print(f"Found {len(greens)} green color declarations:")
    for source, path, line_num, color, line_content in greens:
        print(f"[{source}] {os.path.basename(path)}:L{line_num} -> {color} in '{line_content}'")

if __name__ == '__main__':
    find_greens()
