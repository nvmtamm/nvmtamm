import cv2
import numpy as np
import os
import json

SRC_IMG_PATH = "assets/original-footer.png"
ASSETS_ICONS_DIR = "assets/interactive-icons"
DOCS_ICONS_DIR = "docs/assets/icons"
GALLERY_DIR = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/clean_gallery"

os.makedirs(ASSETS_ICONS_DIR, exist_ok=True)
os.makedirs(DOCS_ICONS_DIR, exist_ok=True)
os.makedirs(GALLERY_DIR, exist_ok=True)

img = cv2.imread(SRC_IMG_PATH)
H, W, _ = img.shape

# Cosmic background detector
def is_bg(b, g, r):
    # cosmic navy background is ~ B=41, G=10, R=3
    dist = np.sqrt((b.astype(float) - 41.0)**2 + (g.astype(float) - 10.0)**2 + (r.astype(float) - 3.0)**2)
    return (dist < 22) | ((b < 48) & (g < 18) & (r < 15))

def finish_sprite(crop, mask):
    mask = mask.astype(np.uint8)
    # Smooth edges with 3x3 gaussian blur for antialiasing
    mask_smooth = cv2.GaussianBlur(mask, (3, 3), 0)
    
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = mask_smooth
    
    # Crop to non-transparent bounding box
    alpha = rgba[:, :, 3]
    ys, xs = np.where(alpha > 12)
    if len(xs) > 0 and len(ys) > 0:
        x_min, x_max = np.min(xs), np.max(xs)
        y_min, y_max = np.min(ys), np.max(ys)
        final_crop = rgba[y_min:y_max+1, x_min:x_max+1]
        offset_x = x_min
        offset_y = y_min
    else:
        final_crop = rgba
        offset_x = 0
        offset_y = 0
        
    return final_crop, offset_x, offset_y

records = []

def save_icon(icon_id, name, crop, mask, global_x, global_y, z_index=2):
    sprite, ox, oy = finish_sprite(crop, mask)
    sh, sw = sprite.shape[:2]
    
    p1 = os.path.join(ASSETS_ICONS_DIR, f"{icon_id}.png")
    p2 = os.path.join(DOCS_ICONS_DIR, f"{icon_id}.png")
    p_gal = os.path.join(GALLERY_DIR, f"{icon_id}.png")
    
    cv2.imwrite(p1, sprite)
    cv2.imwrite(p2, sprite)
    cv2.imwrite(p_gal, sprite)
    
    cx = float(global_x + ox + sw / 2.0)
    cy = float(global_y + oy + sh / 2.0)
    
    records.append({
        "id": icon_id,
        "name": name,
        "src": f"assets/icons/{icon_id}.png",
        "width": int(sw),
        "height": int(sh),
        "radius": int(max(sw, sh) / 2),
        "origX": round(cx, 1),
        "origY": round(cy, 1),
        "normX": round(cx / W, 4),
        "normY": round(cy / H, 4),
        "origLeft": round(float(global_x + ox), 1),
        "origTop": round(float(global_y + oy), 1),
        "zIndex": z_index
    })
    print(f"Extracted {icon_id:18s} -> {sw:3d}x{sh:3d} at ({cx:.1f}, {cy:.1f})")

print("Processing clean extractions...")
