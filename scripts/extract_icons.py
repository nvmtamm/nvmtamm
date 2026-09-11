import cv2
import json
import numpy as np
import os
from catalog_config import ICONS_CATALOG

SRC_IMG = "/Users/nguyenvanminhtam/nvmtamm/assets/original-footer.png"
OUT_DIR = "/Users/nguyenvanminhtam/nvmtamm/assets/interactive-icons"
DOCS_ICONS_DIR = "/Users/nguyenvanminhtam/nvmtamm/docs/assets/icons"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DOCS_ICONS_DIR, exist_ok=True)

img = cv2.imread(SRC_IMG)
H, W = img.shape[:2]

def clean_and_extract_sprite(img, item, padding=4):
    x1, y1, x2, y2 = item["rect"]
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(W, x2 + padding)
    y2 = min(H, y2 + padding)
    
    crop = img[y1:y2, x1:x2].copy()
    ch, cw = crop.shape[:2]
    
    # Calculate background mask:
    # Deep blue / dark navy background
    # B < 68, G < 40, R < 40, or brightness < 45
    b = crop[:, :, 0].astype(np.float32)
    g = crop[:, :, 1].astype(np.float32)
    r = crop[:, :, 2].astype(np.float32)
    
    # Brightness / max channel
    max_c = np.maximum(np.maximum(b, g), r)
    # Background distance from dark navy [45, 15, 8]
    bg_dist = np.sqrt((b - 45)**2 + (g - 15)**2 + (r - 8)**2)
    
    # Probable background
    bg_prob = (max_c < 48) | (bg_dist < 32)
    
    # Refined GrabCut
    mask = np.full((ch, cw), cv2.GC_PR_FGD, dtype=np.uint8)
    
    # Border pixels that match background
    for y in range(ch):
        for x in range(cw):
            if (x < 2 or x >= cw - 2 or y < 2 or y >= ch - 2) and bg_prob[y, x]:
                mask[y, x] = cv2.GC_BGD
            elif bg_prob[y, x]:
                mask[y, x] = cv2.GC_PR_BGD
                
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    try:
        cv2.grabCut(crop, mask, None, bgdModel, fgdModel, 3, cv2.GC_INIT_WITH_MASK)
        fg_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    except Exception:
        fg_mask = ((~bg_prob) * 255).astype(np.uint8)
        
    # Morphological cleaning to remove tiny specks/stars outside the icon
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    
    # Anti-alias mask with feathering
    fg_mask = cv2.GaussianBlur(fg_mask, (3, 3), 0)
    
    # Combine RGBA
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = fg_mask
    
    # Crop to content bounds
    alpha = rgba[:, :, 3]
    ys, xs = np.where(alpha > 15)
    if len(xs) > 0 and len(ys) > 0:
        min_x, max_x = np.min(xs), np.max(xs)
        min_y, max_y = np.min(ys), np.max(ys)
        final_sprite = rgba[min_y:max_y+1, min_x:max_x+1]
        sprite_w = max_x - min_x + 1
        sprite_h = max_y - min_y + 1
    else:
        final_sprite = rgba
        sprite_w = cw
        sprite_h = ch
        
    name = item["name"]
    out_path1 = os.path.join(OUT_DIR, f"{name}.png")
    out_path2 = os.path.join(DOCS_ICONS_DIR, f"{name}.png")
    cv2.imwrite(out_path1, final_sprite)
    cv2.imwrite(out_path2, final_sprite)
    
    # Metadata for physics engine
    orig_center_x = (item["rect"][0] + item["rect"][2]) / 2.0
    orig_center_y = (item["rect"][1] + item["rect"][3]) / 2.0
    
    return {
        "id": name,
        "name": item["title"],
        "src": f"assets/icons/{name}.png",
        "width": int(sprite_w),
        "height": int(sprite_h),
        "radius": int(max(sprite_w, sprite_h) / 2),
        "origX": float(orig_center_x),
        "origY": float(orig_center_y),
        "normX": float(orig_center_x / W),
        "normY": float(orig_center_y / H),
    }

def generate_clean_backdrop(img):
    # Create clean cosmic backdrop:
    # Left circuit: x 0..110
    # Right circuit: x 910..1024
    # Center: fill with smooth deep navy starry sky
    backdrop = img.copy()
    
    # Sample dark starry sky from clear areas
    sky_sample = img[10:40, 480:520]
    mean_color = sky_sample.mean(axis=(0, 1)).astype(np.uint8)
    
    # Inpaint or blend center area (100 to 920) with dark cosmic gradient + random subtle stars
    center_w = 920 - 100
    noise = np.random.normal(0, 3, (H, center_w, 3))
    base_bg = np.zeros((H, center_w, 3), dtype=np.float32)
    # Deep space blue gradient: top is slightly darker, center has slight cyan nebular glow
    for y in range(H):
        ratio = y / H
        base_bg[y, :, 0] = 38 + 10 * np.sin(ratio * np.pi) # B
        base_bg[y, :, 1] = 14 + 6 * np.sin(ratio * np.pi)  # G
        base_bg[y, :, 2] = 8 + 4 * np.sin(ratio * np.pi)   # R
        
    center_bg = np.clip(base_bg + noise, 0, 255).astype(np.uint8)
    
    # Add scattered tiny stars
    num_stars = 80
    for _ in range(num_stars):
        sx = np.random.randint(0, center_w)
        sy = np.random.randint(0, H)
        bright = np.random.randint(140, 255)
        center_bg[sy, sx] = [bright, bright, bright]
        if np.random.rand() > 0.7 and sy + 1 < H and sx + 1 < center_w:
            center_bg[sy+1, sx] = [bright // 2, bright // 2, bright // 2]
            
    # Soft blend edges into circuit areas
    blend_width = 30
    for i in range(blend_width):
        alpha = i / float(blend_width)
        # left seam (around x=100)
        backdrop[:, 100 + i] = (1 - alpha) * backdrop[:, 100 + i] + alpha * center_bg[:, i]
        # right seam (around x=920)
        backdrop[:, 920 - blend_width + i] = alpha * backdrop[:, 920 - blend_width + i] + (1 - alpha) * center_bg[:, center_w - blend_width + i]
        
    backdrop[:, 100 + blend_width : 920 - blend_width] = center_bg[:, blend_width : center_w - blend_width]
    
    cv2.imwrite("/Users/nguyenvanminhtam/nvmtamm/assets/footer-backdrop.png", backdrop)
    cv2.imwrite("/Users/nguyenvanminhtam/nvmtamm/docs/assets/backdrop.png", backdrop)
    print("Saved footer-backdrop.png")

metadata_list = []
print(f"Extracting {len(ICONS_CATALOG)} icons...")
for item in ICONS_CATALOG:
    meta = clean_and_extract_sprite(img, item)
    metadata_list.append(meta)

generate_clean_backdrop(img)

# Save metadata.json
meta_data = {
    "bannerWidth": W,
    "bannerHeight": H,
    "totalIcons": len(metadata_list),
    "icons": metadata_list
}

with open("/Users/nguyenvanminhtam/nvmtamm/assets/icons-metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta_data, f, indent=2, ensure_ascii=False)

with open("/Users/nguyenvanminhtam/nvmtamm/docs/assets/icons-metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta_data, f, indent=2, ensure_ascii=False)

print(f"Extraction complete! Extracted {len(metadata_list)} icons and metadata.")
