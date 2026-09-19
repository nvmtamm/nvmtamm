import cv2
import numpy as np
import json

img_orig = cv2.imread("assets/original-footer.png")
H, W, _ = img_orig.shape

backdrop = cv2.imread("assets/footer-backdrop.png")
if backdrop is None or backdrop.shape != img_orig.shape:
    backdrop = img_orig.copy()
    backdrop[:, 115:915] = [40, 8, 2]

with open("assets/icons-metadata.json") as f:
    meta = json.load(f)

icons = meta["icons"] if isinstance(meta, dict) and "icons" in meta else meta
# Sort by zIndex
icons.sort(key=lambda x: x.get("zIndex", 1))

reconstructed = backdrop.copy()

for item in icons:
    sprite_path = f"assets/interactive-icons/{item['id']}.png"
    sprite = cv2.imread(sprite_path, cv2.IMREAD_UNCHANGED)
    if sprite is None:
        continue
    
    sh, sw = sprite.shape[:2]
    x = int(round(item["origLeft"]))
    y = int(round(item["origTop"]))
    
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(W, x + sw), min(H, y + sh)
    
    crop_sx1 = x1 - x
    crop_sy1 = y1 - y
    crop_sx2 = crop_sx1 + (x2 - x1)
    crop_sy2 = crop_sy1 + (y2 - y1)
    
    sub_sp = sprite[crop_sy1:crop_sy2, crop_sx1:crop_sx2]
    alpha = sub_sp[:, :, 3].astype(float) / 255.0
    alpha_3d = np.stack([alpha, alpha, alpha], axis=2)
    
    bg_roi = reconstructed[y1:y2, x1:x2].astype(float)
    fg_roi = sub_sp[:, :, :3].astype(float)
    
    blended = alpha_3d * fg_roi + (1.0 - alpha_3d) * bg_roi
    reconstructed[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)

comparison = np.vstack([img_orig, reconstructed])
out_path = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/compare_original_reconstructed.png"
cv2.imwrite(out_path, comparison)
cv2.imwrite("assets/footer-physics-preview.png", reconstructed)
cv2.imwrite("docs/assets/footer-physics-preview.png", reconstructed)
print("Saved comparison image successfully!")
