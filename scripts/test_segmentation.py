import cv2
import numpy as np
import os

img = cv2.imread("assets/original-footer.png")
H, W, _ = img.shape

# Helper to check cosmic background color
def is_cosmic_bg(b, g, r):
    # Dark space
    dist = np.sqrt((b - 40.0)**2 + (g - 9.0)**2 + (r - 4.0)**2)
    return (dist < 28) | ((b < 55) & (g < 25) & (r < 22))

def extract_with_contour(crop, seed_mask, smooth=True):
    # Flood fill or contour from seed_mask
    h, w = crop.shape[:2]
    b = crop[:, :, 0].astype(np.float32)
    g = crop[:, :, 1].astype(np.float32)
    r = crop[:, :, 2].astype(np.float32)
    
    bg = is_cosmic_bg(b, g, r)
    
    # We want a mask where seed_mask is true, and grows to include any non-bg pixels connected to it
    # Dilate seed slightly then take intersection with non-bg
    mask = seed_mask.astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_mask = np.zeros((h, w), dtype=np.uint8)
    for c in contours:
        if cv2.contourArea(c) > 20:
            cv2.drawContours(final_mask, [c], -1, 255, -1)
            
    # For any pixel inside the contour that was black (like eyes or inner black lines), keep it!
    # Only remove true background outside
    if smooth:
        final_mask = cv2.GaussianBlur(final_mask, (3, 3), 0)
        
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = final_mask
    return rgba

out_dir = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/test_extracted"
os.makedirs(out_dir, exist_ok=True)

# 1. GitHub: White disc + Octocat
# Crop: 222, 86, 282, 146
crop_gh = img[86:146, 222:282].copy()
gh_h, gh_w = crop_gh.shape[:2]
# Center of circle relative to crop:
# In full image: cx=252, cy=116 -> in crop: cx=30, cy=30, r=28
mask_gh = np.zeros((gh_h, gh_w), dtype=np.uint8)
cv2.circle(mask_gh, (30, 30), 28, 255, -1)
mask_gh = cv2.GaussianBlur(mask_gh, (3, 3), 0)
rgba_gh = cv2.cvtColor(crop_gh, cv2.COLOR_BGR2BGRA)
rgba_gh[:, :, 3] = mask_gh
cv2.imwrite(f"{out_dir}/github.png", rgba_gh)

# 2. Gopher Mascot
# Full image box: 450, 102, 558, 204
crop_g = img[102:204, 450:558].copy()
gh, gw = crop_g.shape[:2]
b = crop_g[:, :, 0].astype(int)
g = crop_g[:, :, 1].astype(int)
r = crop_g[:, :, 2].astype(int)
# Gopher body: cyan (b>140, g>120, r<140) or white eyes (b>180, g>180, r>180)
# Exclude left side x < 18 where JS (r>180, g>180) touches
gopher_seed = ((b > 120) & (g > 100)) & ~((r > 160) & (g > 160) & (b < 100))
# Mask out x < 15 to avoid JS
gopher_seed[:, :16] = False
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
gopher_dil = cv2.dilate(gopher_seed.astype(np.uint8), kernel)
contours, _ = cv2.findContours(gopher_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
mask_g = np.zeros((gh, gw), dtype=np.uint8)
for c in contours:
    if cv2.contourArea(c) > 1500:
        cv2.drawContours(mask_g, [c], -1, 255, -1)
# Keep bottom flat or natural
mask_g = cv2.GaussianBlur(mask_g, (3, 3), 0)
rgba_g = cv2.cvtColor(crop_g, cv2.COLOR_BGR2BGRA)
rgba_g[:, :, 3] = mask_g
cv2.imwrite(f"{out_dir}/gopher_mascot.png", rgba_g)

# 3. Docker Whale
crop_d = img[53:146, 280:390].copy()
dh, dw = crop_d.shape[:2]
b = crop_d[:, :, 0].astype(int)
g = crop_d[:, :, 1].astype(int)
r = crop_d[:, :, 2].astype(int)
# Whale is blue/cyan: b > 110, and not orange (r > 160), not white disc (r>200, g>200, b>200 at left x<20)
docker_seed = (b > 100) & ~((r > 160) & (g > 80)) & ~((r > 190) & (g > 190) & (b > 190) & (np.arange(dw)[None, :] < 20))
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
docker_dil = cv2.dilate(docker_seed.astype(np.uint8), kernel)
contours, _ = cv2.findContours(docker_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
mask_d = np.zeros((dh, dw), dtype=np.uint8)
for c in contours:
    if cv2.contourArea(c) > 2000:
        cv2.drawContours(mask_d, [c], -1, 255, -1)
mask_d = cv2.GaussianBlur(mask_d, (3, 3), 0)
rgba_d = cv2.cvtColor(crop_d, cv2.COLOR_BGR2BGRA)
rgba_d[:, :, 3] = mask_d
cv2.imwrite(f"{out_dir}/docker.png", rgba_d)

# 4. Xcode AppStore + Hammer
crop_x = img[106:204, 790:905].copy()
xh, xw = crop_x.shape[:2]
b = crop_x[:, :, 0].astype(int)
g = crop_x[:, :, 1].astype(int)
r = crop_x[:, :, 2].astype(int)
# Xcode blueprint is blue (b > 130, r < 100), hammer handle is dark (b<60, g<60, r<60), hammer head is metal
# Exclude left MySQL (x < 15, y > 40)
xcode_seed = (b > 80) | ((b < 60) & (g < 60) & (r < 60)) | (r > 70)
# But exclude dark cosmic space
bg = is_cosmic_bg(b, g, r)
xcode_seed = (~bg) & (np.arange(xw)[None, :] > 10)
# Clean specks
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
xcode_dil = cv2.dilate(xcode_seed.astype(np.uint8), kernel)
contours, _ = cv2.findContours(xcode_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
mask_x = np.zeros((xh, xw), dtype=np.uint8)
for c in contours:
    if cv2.contourArea(c) > 3000:
        cv2.drawContours(mask_x, [c], -1, 255, -1)
mask_x = cv2.GaussianBlur(mask_x, (3, 3), 0)
rgba_x = cv2.cvtColor(crop_x, cv2.COLOR_BGR2BGRA)
rgba_x[:, :, 3] = mask_x
cv2.imwrite(f"{out_dir}/xcode_appstore.png", rgba_x)

print("Saved test icons!")
