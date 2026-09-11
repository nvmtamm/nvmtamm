import cv2
import numpy as np
import os

img = cv2.imread("/Users/nguyenvanminhtam/nvmtamm/assets/original-footer.png")

def extract_sprite(img, rect, name, padding=3):
    x1, y1, x2, y2 = rect
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(img.shape[1], x2 + padding)
    y2 = min(img.shape[0], y2 + padding)
    
    crop = img[y1:y2, x1:x2].copy()
    ch, cw = crop.shape[:2]
    
    # Identify background pixels
    # The background is dark navy: R < 35, G < 35, B < 65
    # or hue in blue range with low saturation/val
    b, g, r = crop[:,:,0], crop[:,:,1], crop[:,:,2]
    bg_prob = (b < 65) & (g < 40) & (r < 40)
    
    # Also create grabcut mask
    mask = np.full((ch, cw), cv2.GC_PR_FGD, dtype=np.uint8)
    # Mark definite bg on outer 2px border if they match dark color
    for y in range(ch):
        for x in range(cw):
            if (x < 2 or x >= cw-2 or y < 2 or y >= ch-2) and bg_prob[y, x]:
                mask[y, x] = cv2.GC_BGD
            elif bg_prob[y, x]:
                mask[y, x] = cv2.GC_PR_BGD
                
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    try:
        cv2.grabCut(crop, mask, None, bgdModel, fgdModel, 3, cv2.GC_INIT_WITH_MASK)
        fg_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    except Exception as e:
        # Fallback to color thresholding
        fg_mask = ((~bg_prob) * 255).astype(np.uint8)
        
    # Smooth edges with slight blur for anti-aliasing
    fg_mask = cv2.GaussianBlur(fg_mask, (3, 3), 0)
    
    # Create RGBA
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = fg_mask
    
    # Crop to non-transparent bounding box
    alpha = rgba[:, :, 3]
    ys, xs = np.where(alpha > 20)
    if len(xs) > 0 and len(ys) > 0:
        min_x, max_x = np.min(xs), np.max(xs)
        min_y, max_y = np.min(ys), np.max(ys)
        final_sprite = rgba[min_y:max_y+1, min_x:max_x+1]
    else:
        final_sprite = rgba
        
    os.makedirs("/Users/nguyenvanminhtam/nvmtamm/assets/interactive-icons", exist_ok=True)
    out_path = f"/Users/nguyenvanminhtam/nvmtamm/assets/interactive-icons/{name}.png"
    cv2.imwrite(out_path, final_sprite)
    print(f"Saved {name}: shape={final_sprite.shape}")

# Test on 3 icons
extract_sprite(img, (280, 70, 380, 155), "docker")
extract_sprite(img, (440, 145, 540, 204), "gopher_main")
extract_sprite(img, (690, 25, 750, 95), "react")
