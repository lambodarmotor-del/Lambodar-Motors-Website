def consolidate_border_radius():
    css_path = "assets/css/style.css"
    with open(css_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Maps of exact line number (1-based index) to replaced content
    replacements = {
        105: "  border-radius: 6px;\n", # .badge (small)
        119: "  border-radius: var(--border-radius);\n", # .owner-profile-container (standard)
        147: "  border-radius: var(--border-radius);\n", # .owner-image-wrapper (standard)
        210: "  border-radius: var(--border-radius);\n", # .btn (standard)
        508: "  border-radius: var(--border-radius);\n", # .service-card (standard)
        614: "  border-radius: 6px;\n", # .service-card-price (small)
        640: "  border-radius: var(--border-radius);\n", # .slider-container-box (standard)
        917: "  border-radius: var(--border-radius);\n", # .gallery-lightbox-content (standard)
        1025: "  border-radius: var(--border-radius);\n", # .zoom-lightbox-content (standard)
        1079: "  border-radius: 6px;\n", # .reviews-badge/tag (small)
        1161: "  border-radius: var(--border-radius);\n", # #contactForm input etc (standard)
        1188: "  border-radius: var(--border-radius);\n", # #contactForm button (standard)
        1208: "  border-radius: var(--border-radius);\n", # .faq-item (standard)
        1502: "  border-radius: 0 var(--border-radius) var(--border-radius) 0;\n", # blockquote
        1645: "  border-radius: var(--border-radius);\n", # .faq-static-item (standard)
        1713: "  border-radius: var(--border-radius);\n", # dropdown-menu (standard)
        1844: "  border-radius: var(--border-radius);\n", # .owner-value (standard)
        1997: "  border-radius: var(--border-radius);\n", # duplicate owner-profile-container (standard)
        2020: "  border-radius: var(--border-radius);\n", # .owner-image-wrapper (standard)
        2299: "  border-radius: 0 0 var(--border-radius) 0;\n", # .skip-to-content (standard button size)
        2397: "  border-radius: var(--border-radius);\n", # .faq-more-btn (standard)
        2427: "  border-radius: var(--border-radius);\n", # .map-iframe-custom (standard)
    }
    
    updated = 0
    for idx, new_content in replacements.items():
        # idx is 1-based, list is 0-based
        line_idx = idx - 1
        if line_idx < len(lines):
            old_line = lines[line_idx]
            if "border-radius" in old_line:
                lines[line_idx] = new_content
                updated += 1
            else:
                print(f"Warning: Line {idx} does not contain 'border-radius': {old_line.strip()}")
                
    with open(css_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    print(f"Successfully consolidated {updated} border-radius rules in style.css!")

if __name__ == "__main__":
    consolidate_border_radius()
