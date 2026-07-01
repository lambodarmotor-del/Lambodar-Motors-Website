import re

def clean_inline_styles():
    idx_path = "index.html"
    with open(idx_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Trust Stats bar
    content = content.replace(
        '<div style="background:#0f0f12; border-bottom: 1px solid rgba(255, 255, 255, 0.03);">',
        '<div class="trust-stats-bar">'
    )
    content = content.replace(
        '<div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px; padding: 10px 24px;">',
        '<div class="trust-stats-container">'
    )
    content = content.replace(
        '<div style="text-align:center; flex: 1; min-width: 180px;">',
        '<div class="trust-stat-item">'
    )
    # Match both #FF4D4D and updated var(--accent-red)
    content = re.sub(
        r'<div style="font-size:28px;\s*font-weight:700;\s*color:#FF4D4D;\s*margin-bottom:\s*2px;">',
        '<div class="trust-stat-number">',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'<div style="font-size:28px;\s*font-weight:700;\s*color:var\(--accent-red\);\s*margin-bottom:\s*2px;">',
        '<div class="trust-stat-number">',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'<div style="font-size:13px;\s*color:#a0aec0;">',
        '<div class="trust-stat-label">',
        content,
        flags=re.IGNORECASE
    )
    
    # 2. CTA section padding/colors
    content = re.sub(
        r'<section class="cta-section"\s+style="text-align:center;\s*padding:\s*80px\s+20px;\s*background:#16161a;">',
        '<section class="cta-section cta-section-custom">',
        content
    )
    
    # 3. Hero subtitle font size/color & description
    content = re.sub(
        r'<span style="font-size:\s*0.6em;\s*display:\s*block;\s*margin-top:\s*10px;\s*font-weight:\s*600;\s*color:\s*#a0aec0;">',
        '<span class="hero-h1-subtitle">',
        content
    )
    content = re.sub(
        r'<p style="font-size:\s*17px;\s*color:\s*#a0aec0;\s*margin-top:\s*15px;\s*margin-bottom:\s*24px;\s*font-weight:\s*500;\s*font-family:\s*var\(--font-family\);\s*line-height:\s*1.6;\s*max-width:\s*650px;">',
        '<p class="hero-description">',
        content
    )
    
    # 4. FAQ container, heading and button styles
    content = content.replace(
        '<div class="faq-container" style="max-width: 800px; margin: 60px auto 0 auto; display: flex; flex-direction: column; gap: 20px;">',
        '<div class="faq-container faq-container-custom">'
    )
    content = content.replace(
        '<h3 style="text-align: center; margin-bottom: 15px; font-size: 28px; font-weight: 800;">Frequently Asked Questions</h3>',
        '<h3 class="faq-heading-custom">Frequently Asked Questions</h3>'
    )
    content = content.replace(
        '<div style="text-align: center; margin-top: 35px;">',
        '<div class="faq-more-btn-wrapper">'
    )
    content = re.sub(
        r'<a href="faq.html" class="btn btn-outline" style="border: 2px solid var\(--accent-red\); color: var\(--text-white\); padding: 12px 28px; border-radius: 8px; font-weight: 700; font-family: var\(--font-family\); font-size: 15px; display: inline-flex; align-items: center; gap: 8px; transition: var\(--transition\);">',
        '<a href="faq.html" class="btn btn-outline faq-more-btn">',
        content
    )
    
    # 5. Footer tagline styles
    content = re.sub(
        r'<p class="footer-tagline" style="font-size: 13px; color: #a0aec0; margin-top: 10px; margin-bottom: 15px; font-family: var\(--font-family\); line-height: 1.4;">',
        '<p class="footer-tagline">',
        content
    )
    
    # 6. Map container styles & iframe
    content = content.replace(
        '<div style="width: 100%; height: 100%; min-height: 380px;">',
        '<div class="map-container-custom">'
    )
    content = content.replace(
        'style="border:0; border-radius:12px; filter: brightness(0.8); min-height: 380px;"',
        'class="map-iframe-custom"'
    )
    
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully replaced inline styles in index.html with CSS classes!")

if __name__ == "__main__":
    clean_inline_styles()
