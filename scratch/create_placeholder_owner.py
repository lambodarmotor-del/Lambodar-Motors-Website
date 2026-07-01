import os
from PIL import Image, ImageDraw, ImageFont

def create_owner_placeholder():
    # Define size and color scheme matching the website's dark garage theme
    size = (600, 600)
    bg_color = (22, 22, 26)       # var(--bg-dark)
    accent_color = (185, 28, 28)  # var(--accent-red)
    text_color = (160, 174, 192)  # var(--text-gray)
    title_color = (255, 255, 255) # var(--text-white)
    
    # Create image
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw an elegant red circle border for a silhouette representation
    circle_center = (300, 260)
    circle_radius = 120
    draw.ellipse([circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                  circle_center[0] + circle_radius, circle_center[1] + circle_radius],
                 outline=accent_color, width=4)
                 
    # Draw simple silhouette head and shoulders inside the circle
    # Head
    draw.ellipse([circle_center[0] - 50, circle_center[1] - 70,
                  circle_center[0] + 50, circle_center[1] + 20],
                 fill=text_color)
    # Shoulders
    draw.chord([circle_center[0] - 100, circle_center[1] + 10,
                circle_center[0] + 100, circle_center[1] + 140],
               start=180, end=360, fill=text_color)
               
    # Draw some placeholder text at the bottom
    # Use default font or try to load a system font
    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_sub = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    draw.text((300, 430), "SHAILESH BHAI", fill=title_color, anchor="mm", font=font_title)
    draw.text((300, 480), "[ Profile Photo Generation Pending ]", fill=accent_color, anchor="mm", font=font_sub)
    draw.text((300, 520), "(Will update automatically at 2:05 AM)", fill=text_color, anchor="mm", font=font_sub)
    
    # Ensure directory exists and save
    target_path = r'c:\Users\Harshil\OneDrive\Desktop\website\assets\images\owner.png'
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    img.save(target_path)
    print(f"Temporary placeholder owner image saved to {target_path}")

if __name__ == '__main__':
    create_owner_placeholder()
