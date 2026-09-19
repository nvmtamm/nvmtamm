import cv2
import numpy as np
import os
import json

SRC_IMG_PATH = "assets/original-footer.png"
ASSETS_DIR = "assets/interactive-icons"
DOCS_DIR = "docs/assets/icons"
GALLERY_DIR = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/clean_gallery"

for d in [ASSETS_DIR, DOCS_DIR, GALLERY_DIR]:
    os.makedirs(d, exist_ok=True)

img = cv2.imread(SRC_IMG_PATH)
H, W, _ = img.shape

def is_cosmic(b, g, r):
    # cosmic navy background is ~ B=41, G=10, R=3
    dist = np.sqrt((b.astype(float) - 41.0)**2 + (g.astype(float) - 10.0)**2 + (r.astype(float) - 3.0)**2)
    return (dist < 24) | ((b < 50) & (g < 20) & (r < 18))

def process_and_save(icon_id, title, y1, y2, x1, x2, custom_mask_fn=None, z_index=2):
    crop = img[y1:y2, x1:x2].copy()
    ch, cw, _ = crop.shape
    b, g, r = crop[:, :, 0], crop[:, :, 1], crop[:, :, 2]
    
    if custom_mask_fn is not None:
        mask = custom_mask_fn(crop, b, g, r)
    else:
        mask = (~is_cosmic(b, g, r)).astype(np.uint8) * 255
        # Clean small noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Smooth edges for antialiasing
    mask_smooth = cv2.GaussianBlur(mask.astype(np.uint8), (3, 3), 0)
    
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = mask_smooth
    
    # Crop to non-transparent bounding box
    alpha = rgba[:, :, 3]
    ys, xs = np.where(alpha > 15)
    if len(xs) > 0 and len(ys) > 0:
        min_x, max_x = np.min(xs), np.max(xs)
        min_y, max_y = np.min(ys), np.max(ys)
        final_sprite = rgba[min_y:max_y+1, min_x:max_x+1]
        ox = min_x
        oy = min_y
    else:
        final_sprite = rgba
        ox = 0
        oy = 0
        
    sh, sw = final_sprite.shape[:2]
    p1 = os.path.join(ASSETS_DIR, f"{icon_id}.png")
    p2 = os.path.join(DOCS_DIR, f"{icon_id}.png")
    p_gal = os.path.join(GALLERY_DIR, f"{icon_id}.png")
    
    cv2.imwrite(p1, final_sprite)
    cv2.imwrite(p2, final_sprite)
    cv2.imwrite(p_gal, final_sprite)
    
    gx = x1 + ox
    gy = y1 + oy
    cx = float(gx + sw / 2.0)
    cy = float(gy + sh / 2.0)
    
    return {
        "id": icon_id,
        "name": title,
        "src": f"assets/icons/{icon_id}.png",
        "width": int(sw),
        "height": int(sh),
        "radius": int(max(sw, sh) / 2),
        "origX": round(cx, 1),
        "origY": round(cy, 1),
        "normX": round(cx / W, 4),
        "normY": round(cy / H, 4),
        "origLeft": round(float(gx), 1),
        "origTop": round(float(gy), 1),
        "zIndex": z_index
    }

metadata = []

# 1. Gulp cup
def mask_gulp(c, b, g, r):
    m = ~is_cosmic(b, g, r)
    # Straw and cup are red/white
    return (m.astype(np.uint8) * 255)
metadata.append(process_and_save("gulp", "Gulp", 20, 116, 120, 164, mask_gulp, z_index=3))

# 2. Swift
metadata.append(process_and_save("swift", "Swift", 90, 152, 84, 144, z_index=3))

# 3. Cinema 4D (Ribbon 4)
def mask_c4d(c, b, g, r):
    # Blue ribbon
    blue = (b > 110) & (b > r + 30)
    m = blue.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("cinema4d", "Cinema 4D", 18, 134, 162, 252, mask_c4d, z_index=5))

# 4. Debian / Grafana (Sun with spiral)
def mask_debian(c, b, g, r):
    # Keep the entire sun disk (solid filled inside so black spiral is preserved!)
    m = ~is_cosmic(b, g, r)
    m = m.astype(np.uint8) * 255
    # Fill contour interior
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(m)
    cv2.drawContours(filled, cnts, -1, 255, -1)
    return filled
metadata.append(process_and_save("debian", "Debian", 16, 106, 242, 320, mask_debian, z_index=4))

# 5. Fortran F (Orange 3D F)
def mask_fortran(c, b, g, r):
    orange = (r > 120) & (r > b + 30)
    return orange.astype(np.uint8) * 255
metadata.append(process_and_save("fortran_f", "Fortran", 148, 204, 120, 172, mask_fortran, z_index=3))

# 6. Spring Dots
def mask_spring(c, b, g, r):
    cyan = (b > 100) & (g > 70) & (r < 80)
    return cyan.astype(np.uint8) * 255
metadata.append(process_and_save("spring_dots", "Spring", 160, 204, 104, 148, mask_spring, z_index=2))

# 7. Bracket E (<e>)
def mask_bracket_e(c, b, g, r):
    cyan = (b > 120) & (g > 80) & (r < 70)
    return cyan.astype(np.uint8) * 255
metadata.append(process_and_save("bracket_e", "Bracket E", 95, 146, 164, 214, mask_bracket_e, z_index=3))

# 8. Elastic hexagon E
def mask_elastic_hex(c, b, g, r):
    cyan = (b > 100) & (g > 60)
    m = cyan.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("elastic", "Elasticsearch", 125, 204, 164, 252, mask_elastic_hex, z_index=3))

# 9. GitHub (White disc with black Octocat inside!)
def mask_github(c, b, g, r):
    # A circular white disc with radius ~28
    h, w = c.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (w//2, h//2), int(min(w, h)*0.47), 255, -1)
    return mask
metadata.append(process_and_save("github", "GitHub", 92, 154, 222, 282, mask_github, z_index=6))

# 10. Apple logo
def mask_apple(c, b, g, r):
    silver = (b > 90) & (g > 90) & (r > 90)
    m = silver.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("apple", "Apple", 136, 204, 250, 314, mask_apple, z_index=6))

# 11. gRPC
def mask_grpc(c, b, g, r):
    teal = (b > 60) & (g > 40)
    m = (~is_cosmic(b, g, r)) & teal
    return m.astype(np.uint8) * 255
metadata.append(process_and_save("grpc", "gRPC", 14, 68, 320, 448, mask_grpc, z_index=2))

# 12. Docker whale
def mask_docker(c, b, g, r):
    # Whale is cyan/blue, containers are cyan
    m = (b > 80) & (g > 50)
    m |= (b > 70) & (r < 80)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m.astype(np.uint8) * 255, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("docker", "Docker", 70, 144, 282, 390, mask_docker, z_index=7))

# 13. Blue Chevrons
def mask_chevrons(c, b, g, r):
    cyan = (b > 120) & (g > 80) & (r < 80)
    return cyan.astype(np.uint8) * 255
metadata.append(process_and_save("blue_chevrons", "Chevrons", 130, 184, 308, 350, mask_chevrons, z_index=3))

# 14. GitLab (fox head)
def mask_gitlab(c, b, g, r):
    orange = (r > 130) & (r > b + 40)
    return orange.astype(np.uint8) * 255
metadata.append(process_and_save("gitlab", "GitLab", 134, 182, 348, 390, mask_gitlab, z_index=4))

# 15. Git (orange diamond)
def mask_git(c, b, g, r):
    orange = (r > 140) & (r > b + 40)
    m = orange.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("git", "Git", 84, 142, 378, 430, mask_git, z_index=4))

# 16. Wireshark Shark Fin
def mask_wireshark(c, b, g, r):
    blue = (b > 100) & (b > r + 30)
    blue |= (b > 150) & (g > 150) & (r > 150) # white foam
    return blue.astype(np.uint8) * 255
metadata.append(process_and_save("wireshark_fin", "Wireshark", 162, 204, 320, 372, mask_wireshark, z_index=3))

# 17. Blue Cube
def mask_blue_cube(c, b, g, r):
    blue = (b > 90) & (b > r + 20)
    return blue.astype(np.uint8) * 255
metadata.append(process_and_save("blue_cube", "Cube", 154, 204, 365, 418, mask_blue_cube, z_index=3))

# 18. HTML5 Badge
def mask_html5(c, b, g, r):
    badge = (r > 80) & (g > 50) & (b < 120)
    badge |= (r > 150) & (g > 150) & (b > 150) # number 5
    return badge.astype(np.uint8) * 255
metadata.append(process_and_save("html5_badge", "HTML5", 158, 204, 412, 450, mask_html5, z_index=5))

# 19. JavaScript (JS rounded square)
def mask_js(c, b, g, r):
    # Yellow background and black JS letters
    h, w = c.shape[:2]
    # Solid rounded box
    m = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(m, (3, 3), (w-4, h-4), 255, -1)
    return m
metadata.append(process_and_save("javascript", "JavaScript", 138, 186, 394, 444, mask_js, z_index=5))

# 20. Redis (3D red stack)
def mask_redis(c, b, g, r):
    red = (r > 120) & (r > b + 40)
    red |= (r > 140) & (g > 140) & (b > 140) # white cubes on top
    m = red.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("redis", "Redis", 80, 146, 426, 486, mask_redis, z_index=4))

# 21. Photoshop (Ps)
def mask_ps(c, b, g, r):
    h, w = c.shape[:2]
    m = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(m, (2, 2), (w-3, h-3), 255, -1)
    return m
metadata.append(process_and_save("photoshop", "Photoshop", 60, 114, 446, 496, mask_ps, z_index=3))

# 22. npm (3D red banner)
def mask_npm(c, b, g, r):
    red = (r > 110) & (r > b + 30)
    red |= (r > 150) & (g > 150) & (b > 150) # white letters
    m = red.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("npm", "npm", 10, 68, 502, 568, mask_npm, z_index=4))

# 23. GoLand (Square with black interior and GO text)
def mask_goland(c, b, g, r):
    h, w = c.shape[:2]
    m = np.zeros((h, w), dtype=np.uint8)
    # The GoLand box is tilted slightly, let's keep the box interior solid
    cnts, _ = cv2.findContours((~is_cosmic(b, g, r)).astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(m, cnts, -1, 255, -1)
    return m
metadata.append(process_and_save("goland", "GoLand", 64, 128, 486, 548, mask_goland, z_index=5))

# 24. MDN 3D shield
def mask_mdn(c, b, g, r):
    m = (~is_cosmic(b, g, r)).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("mdn", "MDN", 110, 176, 554, 598, mask_mdn, z_index=3))

# 25. Go Speed (Cyan GO with speed lines)
def mask_go_speed(c, b, g, r):
    cyan = (b > 120) & (g > 80)
    return cyan.astype(np.uint8) * 255
metadata.append(process_and_save("go_speed", "Go Speed", 22, 74, 566, 652, mask_go_speed, z_index=3))

# 26. Gopher Mascot (center bottom)
def mask_gopher(c, b, g, r):
    # Go Gopher blue body, white eyes, black pupils, teeth, bowtie
    # Sits at bottom center, preserve full head and chest
    m = (b > 100) & (g > 80) # blue fur
    m |= (b > 150) & (g > 150) & (r > 150) # white eyes/teeth
    # Also black pupils and bowtie
    h, w = c.shape[:2]
    m_full = np.zeros((h, w), dtype=np.uint8)
    cnts, _ = cv2.findContours(m.astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(m_full, cnts, -1, 255, -1)
    return m_full
metadata.append(process_and_save("gopher_mascot", "Go Gopher", 102, 204, 450, 548, mask_gopher, z_index=10))

# 27. Probot (grey robot face)
def mask_probot(c, b, g, r):
    grey = (b > 80) & (g > 80) & (r > 80)
    m = grey.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("probot", "Probot", 18, 76, 648, 700, mask_probot, z_index=3))

# 28. Vim (teal/green V)
def mask_vim(c, b, g, r):
    green = (g > 80) & (g > r + 20)
    return green.astype(np.uint8) * 255
metadata.append(process_and_save("vim", "Vim", 92, 154, 550, 602, mask_vim, z_index=3))

# 29. Jenkins (butler face)
def mask_jenkins(c, b, g, r):
    face = (r > 100) & (g > 80)
    face |= (r > 120) & (b < 80) # red bowtie
    m = face.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("jenkins", "Jenkins", 118, 180, 580, 630, mask_jenkins, z_index=6))

# 30. Jenkins Gear
def mask_gear(c, b, g, r):
    white = (b > 100) & (g > 100) & (r > 100)
    return white.astype(np.uint8) * 255
metadata.append(process_and_save("jenkins_gear", "Gear", 174, 204, 546, 584, mask_gear, z_index=4))

# 31. Red Streaks
def mask_streaks(c, b, g, r):
    red = (r > 100) & (r > b + 30)
    return red.astype(np.uint8) * 255
metadata.append(process_and_save("red_streaks", "Streaks", 180, 204, 615, 674, mask_streaks, z_index=2))

# 32. NGINX (green 3D block text)
def mask_nginx(c, b, g, r):
    green = (g > 80) & (g > b + 20)
    return green.astype(np.uint8) * 255
metadata.append(process_and_save("nginx", "NGINX", 90, 192, 594, 674, mask_nginx, z_index=4))

# 33. Sketch (yellow diamond)
def mask_sketch(c, b, g, r):
    yellow = (r > 140) & (g > 100) & (b < 100)
    return yellow.astype(np.uint8) * 255
metadata.append(process_and_save("sketch", "Sketch", 86, 144, 632, 682, mask_sketch, z_index=4))

# 34. React (cyan atom)
def mask_react(c, b, g, r):
    cyan = (b > 120) & (g > 80)
    return cyan.astype(np.uint8) * 255
metadata.append(process_and_save("react", "React", 16, 76, 706, 756, mask_react, z_index=4))

# 35. PostgreSQL (blue elephant head with white outline)
def mask_postgres(c, b, g, r):
    blue = (b > 100) & (g > 50)
    m = blue.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("postgres", "PostgreSQL", 112, 188, 662, 734, mask_postgres, z_index=6))

# 36. MySQL (dolphin + text)
def mask_mysql(c, b, g, r):
    blue = (b > 90) & (g > 50)
    yellow = (r > 120) & (g > 90) # orange-gold MySQL text
    m = (blue | yellow).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("mysql", "MySQL", 148, 204, 680, 796, mask_mysql, z_index=6))

# 37. Kafka (white circles + kafka text)
def mask_kafka(c, b, g, r):
    white = (b > 110) & (g > 110) & (r > 110)
    m = white.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("kafka", "Kafka", 30, 96, 692, 804, mask_kafka, z_index=4))

# 38. RabbitMQ (orange origami rabbit)
def mask_rabbitmq(c, b, g, r):
    orange = (r > 130) & (r > b + 40)
    m = orange.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("rabbitmq", "RabbitMQ", 104, 176, 736, 802, mask_rabbitmq, z_index=4))

# 39. Elastic puzzle (colorful circles)
def mask_puzzle(c, b, g, r):
    m = (~is_cosmic(b, g, r)).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("elastic_puzzle", "Elastic", 18, 78, 750, 806, mask_puzzle, z_index=3))

# 40. Illustrator (Ai - orange square with yellow Ai)
def mask_ai(c, b, g, r):
    h, w = c.shape[:2]
    m = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(m, (2, 2), (w-3, h-3), 255, -1)
    return m
metadata.append(process_and_save("illustrator", "Illustrator", 12, 54, 806, 850, mask_ai, z_index=3))

# 41. Kubernetes (blue helm wheel)
def mask_k8s(c, b, g, r):
    blue = (b > 110) & (g > 60)
    m = blue.astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("kubernetes", "Kubernetes", 44, 104, 800, 866, mask_k8s, z_index=4))

# 42. Mini Gophers (pair)
def mask_gopher_pair(c, b, g, r):
    m = (~is_cosmic(b, g, r)).astype(np.uint8) * 255
    return m
metadata.append(process_and_save("gopher_pair", "Mini Gophers", 88, 160, 795, 828, mask_gopher_pair, z_index=5))

# 43. Mini Pink Gopher
def mask_pink_gopher(c, b, g, r):
    pink = (r > 130) & (b > 100)
    return pink.astype(np.uint8) * 255
metadata.append(process_and_save("gopher_pink", "Pink Gopher", 106, 156, 844, 872, mask_pink_gopher, z_index=5))

# 44. Blue Eagle
def mask_eagle(c, b, g, r):
    blue = (b > 110) & (g > 80)
    yellow = (r > 120) & (g > 100) # beak/eye
    return (blue | yellow).astype(np.uint8) * 255
metadata.append(process_and_save("eagle_bird", "Eagle", 12, 70, 846, 908, mask_eagle, z_index=3))

# 45. Xcode App Store + Hammer
def mask_xcode(c, b, g, r):
    blue = (b > 100) & (g > 50)
    hammer = (r > 50) & (g > 50) & (b > 50)
    m = (~is_cosmic(b, g, r)).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
metadata.append(process_and_save("xcode_appstore", "Xcode", 110, 204, 792, 902, mask_xcode, z_index=8))

# Save metadata
payload = {
    "bannerWidth": 1024,
    "bannerHeight": 204,
    "icons": metadata
}

with open("assets/icons-metadata.json", "w") as f:
    json.dump(payload, f, indent=2)
with open("docs/assets/icons-metadata.json", "w") as f:
    json.dump(payload, f, indent=2)

print(f"Successfully processed and saved {len(metadata)} clean authentic icons!")
