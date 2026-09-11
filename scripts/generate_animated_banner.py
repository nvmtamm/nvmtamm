import cv2
import json
import numpy as np
from PIL import Image
import os

print("Generating animated physics banner for README footer...")

# Load backdrop and metadata
backdrop = cv2.imread("/Users/nguyenvanminhtam/nvmtamm/assets/footer-backdrop.png")
H, W = backdrop.shape[:2]

with open("/Users/nguyenvanminhtam/nvmtamm/assets/icons-metadata.json", "r") as f:
    meta = json.load(f)

icons_data = meta["icons"]

# Preload icon sprites (RGBA)
icon_sprites = []
for item in icons_data:
    path = os.path.join("/Users/nguyenvanminhtam/nvmtamm/assets/interactive-icons", f"{item['id']}.png")
    if os.path.exists(path):
        sprite = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        icon_sprites.append({
            "id": item["id"],
            "name": item["name"],
            "sprite": sprite,
            "origX": item["origX"],
            "origY": item["origY"],
            "w": item["width"],
            "h": item["height"],
            # Give each icon a unique harmonic phase and frequency for smooth looping
            "phaseX": np.random.uniform(0, np.pi * 2),
            "phaseY": np.random.uniform(0, np.pi * 2),
            "ampX": np.random.uniform(3, 8),
            "ampY": np.random.uniform(4, 10),
            "rotAmp": np.random.uniform(0.04, 0.12),
        })

num_frames = 24
fps = 12
frames = []

for frame_idx in range(num_frames):
    t = (frame_idx / num_frames) * 2 * np.pi
    frame_bg = backdrop.copy()
    
    # Twinkling stars effect on background
    star_overlay = np.zeros_like(frame_bg)
    for i in range(25):
        sx = int((np.sin(i * 13.7) * 0.5 + 0.5) * (W - 200) + 100)
        sy = int((np.cos(i * 9.3) * 0.5 + 0.5) * (H - 40) + 20)
        intensity = int((np.sin(t * 2 + i) * 0.5 + 0.5) * 200 + 55)
        cv2.circle(frame_bg, (sx, sy), 1, (intensity, intensity, intensity), -1)
    
    # Render floating icons
    for item in icon_sprites:
        sprite = item["sprite"]
        sh, sw = sprite.shape[:2]
        
        # Smooth cyclical displacement for seamless loop
        dx = np.sin(t + item["phaseX"]) * item["ampX"]
        dy = np.cos(t + item["phaseY"]) * item["ampY"]
        rot_angle = np.sin(t + item["phaseX"]) * item["rotAmp"] * (180 / np.pi)
        
        cx = item["origX"] + dx
        cy = item["origY"] + dy
        
        # Rotate sprite
        center = (sw / 2.0, sh / 2.0)
        rot_mat = cv2.getRotationMatrix2D(center, rot_angle, 1.0)
        rotated = cv2.warpAffine(sprite, rot_mat, (sw, sh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
        
        # Overlay on frame_bg
        x1 = int(cx - sw / 2.0)
        y1 = int(cy - sh / 2.0)
        x2 = x1 + sw
        y2 = y1 + sh
        
        # Clip to frame
        src_x1 = max(0, -x1)
        src_y1 = max(0, -y1)
        src_x2 = sw - max(0, x2 - W)
        src_y2 = sh - max(0, y2 - H)
        
        dst_x1 = max(0, x1)
        dst_y1 = max(0, y1)
        dst_x2 = min(W, x2)
        dst_y2 = min(H, y2)
        
        if dst_x2 > dst_x1 and dst_y2 > dst_y1:
            overlay_region = rotated[src_y1:src_y2, src_x1:src_x2]
            alpha = overlay_region[:, :, 3] / 255.0
            for c in range(3):
                frame_bg[dst_y1:dst_y2, dst_x1:dst_x2, c] = (
                    alpha * overlay_region[:, :, c] +
                    (1.0 - alpha) * frame_bg[dst_y1:dst_y2, dst_x1:dst_x2, c]
                )
                
    # Convert BGR to RGB for PIL
    rgb_frame = cv2.cvtColor(frame_bg, cv2.COLOR_BGR2RGB)
    pil_frame = Image.fromarray(rgb_frame)
    # Quantize to 256 colors with adaptive palette for crisp small gif
    pil_quant = pil_frame.quantize(colors=256, method=Image.MEDIANCUT)
    frames.append(pil_quant)

# Save as animated GIF
out_gif = "/Users/nguyenvanminhtam/nvmtamm/assets/footer-physics.gif"
frames[0].save(
    out_gif,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / fps),
    loop=0,
    optimize=True
)
print(f"Generated {out_gif}, size={os.path.getsize(out_gif)/1024:.1f} KB")

# Save as animated WebP (ultra crisp and lightweight)
out_webp = "/Users/nguyenvanminhtam/nvmtamm/assets/footer-physics.webp"
frames[0].save(
    out_webp,
    format="WEBP",
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / fps),
    loop=0,
    quality=85,
    method=6
)
print(f"Generated {out_webp}, size={os.path.getsize(out_webp)/1024:.1f} KB")

# Also save high-res static PNG for fallback
cv2.imwrite("/Users/nguyenvanminhtam/nvmtamm/assets/footer-physics-preview.png", frame_bg)
