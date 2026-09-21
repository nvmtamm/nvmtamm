import cv2
import json
import numpy as np
from PIL import Image
import os

print("Generating animated physics banner for README footer...")

# Load backdrop and metadata
backdrop = cv2.imread("assets/footer-backdrop.png")
if backdrop is None:
    backdrop = cv2.imread("assets/original-footer.png")
    backdrop[:, 115:915] = [40, 8, 2]
    
H, W = backdrop.shape[:2]

with open("assets/icons-metadata.json", "r") as f:
    meta = json.load(f)

icons_data = meta["icons"] if isinstance(meta, dict) and "icons" in meta else meta
# Sort icons by zIndex so background layers are drawn first and mascot is on top
icons_data.sort(key=lambda x: x.get("zIndex", 1))

# Bottom-row items that touch the bottom edge of banner
GROUNDED_IDS = {"gopher_mascot", "apple", "html5_badge", "postgres", "mysql", "xcode_appstore", "spring_dots", "blue_cube", "wireshark_fin", "jenkins_gear"}

# Preload icon sprites
icon_sprites = []
for item in icons_data:
    path = os.path.join("assets/interactive-icons", f"{item['id']}.png")
    if os.path.exists(path):
        sprite_raw = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        tw = int(item["width"])
        th = int(item["height"])
        if sprite_raw.shape[:2] != (th, tw):
            sprite = cv2.resize(sprite_raw, (tw, th), interpolation=cv2.INTER_AREA)
        else:
            sprite = sprite_raw
            
        is_grounded = item["id"] in GROUNDED_IDS
        icon_sprites.append({
            "id": item["id"],
            "name": item["name"],
            "sprite": sprite,
            "origX": item["origX"],
            "origY": item["origY"],
            "origLeft": item["origLeft"],
            "origTop": item["origTop"],
            "w": tw,
            "h": th,
            "phaseX": np.random.uniform(0, np.pi * 2),
            "phaseY": np.random.uniform(0, np.pi * 2),
            "ampX": np.random.uniform(0.5, 1.2) if is_grounded else np.random.uniform(0.8, 1.8),
            "ampY": np.random.uniform(0.1, 0.4) if is_grounded else np.random.uniform(0.8, 1.8),
            "rotAmp": 0.003 if is_grounded else np.random.uniform(0.01, 0.025),
        })

num_frames = 24
fps = 12
frames = []

for frame_idx in range(num_frames):
    t = (frame_idx / num_frames) * 2 * np.pi
    frame_bg = backdrop.copy()
    
    # Twinkling stars effect on background
    for i in range(25):
        sx = int((np.sin(i * 13.7) * 0.5 + 0.5) * (W - 220) + 110)
        sy = int((np.cos(i * 9.3) * 0.5 + 0.5) * (H - 40) + 20)
        intensity = int((np.sin(t * 2 + i) * 0.5 + 0.5) * 180 + 75)
        cv2.circle(frame_bg, (sx, sy), 1, (intensity, intensity, intensity), -1)
    
    # Render floating icons
    for item in icon_sprites:
        sprite = item["sprite"]
        sh, sw = sprite.shape[:2]
        
        dx = np.sin(t + item["phaseX"]) * item["ampX"]
        dy = np.cos(t + item["phaseY"]) * item["ampY"]
        rot_angle = np.sin(t + item["phaseX"]) * item["rotAmp"] * (180 / np.pi)
        
        cx = item["origX"] + dx
        cy = item["origY"] + dy
        
        # Rotate sprite if needed
        if abs(rot_angle) > 0.1:
            center = (sw / 2.0, sh / 2.0)
            rot_mat = cv2.getRotationMatrix2D(center, rot_angle, 1.0)
            rotated = cv2.warpAffine(sprite, rot_mat, (sw, sh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
        else:
            rotated = sprite
            
        x1 = int(round(cx - sw / 2.0))
        y1 = int(round(cy - sh / 2.0))
        x2 = x1 + sw
        y2 = y1 + sh
        
        dst_x1 = max(0, x1)
        dst_y1 = max(0, y1)
        dst_x2 = min(W, x2)
        dst_y2 = min(H, y2)
        
        src_x1 = dst_x1 - x1
        src_y1 = dst_y1 - y1
        src_x2 = src_x1 + (dst_x2 - dst_x1)
        src_y2 = src_y1 + (dst_y2 - dst_y1)
        
        if dst_x2 > dst_x1 and dst_y2 > dst_y1:
            overlay_region = rotated[src_y1:src_y2, src_x1:src_x2]
            alpha = overlay_region[:, :, 3].astype(float) / 255.0
            alpha_3d = np.stack([alpha, alpha, alpha], axis=2)
            
            bg_roi = frame_bg[dst_y1:dst_y2, dst_x1:dst_x2].astype(float)
            fg_roi = overlay_region[:, :, :3].astype(float)
            
            blended = alpha_3d * fg_roi + (1.0 - alpha_3d) * bg_roi
            frame_bg[dst_y1:dst_y2, dst_x1:dst_x2] = np.clip(blended, 0, 255).astype(np.uint8)
            
    rgb_frame = cv2.cvtColor(frame_bg, cv2.COLOR_BGR2RGB)
    pil_frame = Image.fromarray(rgb_frame)
    pil_quant = pil_frame.quantize(colors=256, method=Image.MEDIANCUT)
    frames.append(pil_quant)

# Save as animated GIF
out_gif = "assets/footer-physics.gif"
frames[0].save(
    out_gif,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / fps),
    loop=0,
    optimize=True
)
print(f"Generated {out_gif}, size={os.path.getsize(out_gif)/1024:.1f} KB")

# Save as animated WebP
out_webp = "assets/footer-physics.webp"
frames[0].save(
    out_webp,
    format="WEBP",
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / fps),
    loop=0,
    quality=88,
    method=6
)
print(f"Generated {out_webp}, size={os.path.getsize(out_webp)/1024:.1f} KB")

# High-res static PNG
cv2.imwrite("assets/footer-physics-preview.png", frame_bg)
cv2.imwrite("docs/assets/footer-physics-preview.png", frame_bg)
print("Updated footer-physics-preview.png!")
