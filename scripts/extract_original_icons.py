import cv2
import numpy as np
import os
import json

SRC_IMG_PATH = "assets/original-footer.png"
ASSETS_ICONS_DIR = "assets/interactive-icons"
DOCS_ICONS_DIR = "docs/assets/icons"
DEBUG_DIR = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/extracted_gallery"

os.makedirs(ASSETS_ICONS_DIR, exist_ok=True)
os.makedirs(DOCS_ICONS_DIR, exist_ok=True)
os.makedirs(DEBUG_DIR, exist_ok=True)

img = cv2.imread(SRC_IMG_PATH)
H, W, _ = img.shape

Z_INDEX_MAP = {
    'gopher_mascot': 10,
    'xcode_appstore': 8,
    'docker': 7,
    'jenkins': 6,
    'postgres': 6,
    'mysql': 6,
    'apple': 6,
    'github': 5,
    'cinema4d': 5,
    'goland': 5,
    'nginx': 4,
    'kafka': 4,
    'kubernetes': 4,
    'rabbitmq': 4,
    'gopher_pair': 5,
    'gopher_pink': 5,
    'javascript': 5,
    'html5_badge': 5,
}

def is_cosmic_bg(b, g, r):
    dist = np.sqrt((b.astype(float) - 40.0)**2 + (g.astype(float) - 9.0)**2 + (r.astype(float) - 4.0)**2)
    return (dist < 26) | ((b < 52) & (g < 24) & (r < 22))

def create_sprite(crop, mask):
    mask = mask.astype(np.uint8)
    mask_smooth = cv2.GaussianBlur(mask, (3, 3), 0)
    
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = mask_smooth
    
    alpha = rgba[:, :, 3]
    ys, xs = np.where(alpha > 10)
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

extracted_results = []

def register(id_name, title, sprite, global_x, global_y):
    sh, sw = sprite.shape[:2]
    center_x = global_x + sw / 2.0
    center_y = global_y + sh / 2.0
    
    p1 = os.path.join(ASSETS_ICONS_DIR, f"{id_name}.png")
    p2 = os.path.join(DOCS_ICONS_DIR, f"{id_name}.png")
    p_debug = os.path.join(DEBUG_DIR, f"{id_name}.png")
    
    cv2.imwrite(p1, sprite)
    cv2.imwrite(p2, sprite)
    cv2.imwrite(p_debug, sprite)
    
    z_idx = Z_INDEX_MAP.get(id_name, 2)
    
    extracted_results.append({
        "id": id_name,
        "name": title,
        "src": f"assets/icons/{id_name}.png",
        "width": int(sw),
        "height": int(sh),
        "radius": int(max(sw, sh) / 2),
        "origX": float(center_x),
        "origY": float(center_y),
        "normX": float(center_x / W),
        "normY": float(center_y / H),
        "origLeft": float(global_x),
        "origTop": float(global_y),
        "zIndex": z_idx
    })

def extract_all():
    global extracted_results
    extracted_results = []

    # ================= TOP ROW =================
    # 1. Gulp
    c = img[10:88, 114:170].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    mask = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    mask[:, 48:] = 0
    sp, ox, oy = create_sprite(c, mask)
    register("gulp", "Gulp", sp, 114 + ox, 10 + oy)

    # 2. Cinema 4D
    c = img[8:105, 160:248].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    ribbon = (b > 130) & (b > r + 30)
    ribbon[88:, :] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(ribbon.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("cinema4d", "Cinema 4D", sp, 160 + ox, 8 + oy)

    # 3. Debian / Grafana
    c = img[5:92, 242:318].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    gear = (r > 120) & (r > b + 30)
    gear |= (r > 200) & (g > 200) & (b > 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dil = cv2.dilate(gear.astype(np.uint8) * 255, kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("debian", "Debian / Grafana", sp, 242 + ox, 5 + oy)

    # 4. gRPC
    c = img[8:62, 316:454].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    teal = (g > 55) & (b > 55) & ~is_cosmic_bg(b, g, r)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx((teal.astype(np.uint8) * 255), cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("grpc", "gRPC", sp, 316 + ox, 8 + oy)

    # 5. Photoshop
    c = img[24:78, 444:495].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    ps = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(ps, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("photoshop", "Photoshop", sp, 444 + ox, 24 + oy)

    # 6. npm
    c = img[0:52, 500:572].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    red_box = (r > 135) & (r > b + 50)
    white_txt = (r > 200) & (g > 200) & (b > 200)
    npm_all = red_box | white_txt
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(npm_all.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("npm", "npm", sp, 500 + ox, 0 + oy)

    # 7. Go Speed (GO with streaks)
    c = img[10:70, 565:674].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    go_cyan = (b > 135) & (g > 115) & (r < 130)
    go_cyan[r > 140] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(go_cyan.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("go_speed", "Go Lang", sp, 565 + ox, 10 + oy)

    # 8. Probot
    c = img[26:80, 648:700].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    robot = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    robot[:, 46:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(robot, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("probot", "Probot", sp, 648 + ox, 26 + oy)

    # 9. React
    c = img[22:82, 692:752].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    atom = (b > 150) & (g > 130)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(atom.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("react", "React", sp, 692 + ox, 22 + oy)

    # 10. Elasticsearch
    c = img[26:84, 750:805].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    elastic = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(elastic, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("elastic", "Elasticsearch", sp, 750 + ox, 26 + oy)

    # 11. Illustrator
    c = img[22:72, 804:854].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    ai = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(ai, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("illustrator", "Illustrator", sp, 804 + ox, 22 + oy)

    # 12. Blue Eagle
    c = img[12:74, 846:912].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    eagle = (b > 130) & (g > 100) & (r < 80)
    eagle |= (~is_cosmic_bg(b, g, r) & (r > 70) & (np.arange(c.shape[1])[None, :] > 35))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(eagle.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("eagle_bird", "Blue Eagle", sp, 846 + ox, 12 + oy)

    # ================= MIDDLE ROW =================
    # 13. Swift
    c = img[84:146, 84:144].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    swift = (r > 160) & (g > 50) & (b < 80)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(swift.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("swift", "Swift", sp, 84 + ox, 84 + oy)

    # 14. Hex Bracket <e>
    c = img[104:166, 152:214].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    hex_e = (b > 150) & (g > 110) & (r < 80)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(hex_e.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("bracket_e", "Hex Code", sp, 152 + ox, 104 + oy)

    # 15. GitHub
    c = img[86:146, 222:282].copy()
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (30, 30), 28, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("github", "GitHub", sp, 222 + ox, 86 + oy)

    # 16. Docker Whale
    c = img[53:146, 280:390].copy()
    dh, dw = c.shape[:2]
    b, g, r = c[:, :, 0].astype(int), c[:, :, 1].astype(int), c[:, :, 2].astype(int)
    docker_seed = (b > 95) & ~((r > 160) & (g > 80)) & ~((r > 190) & (g > 190) & (b > 190) & (np.arange(dw)[None, :] < 20))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dil = cv2.dilate(docker_seed.astype(np.uint8), kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros((dh, dw), dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 2000:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("docker", "Docker", sp, 280 + ox, 53 + oy)

    # 17. Git
    c = img[58:128, 372:436].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    git = (r > 150) & (r > b + 50)
    git |= (r > 200) & (g > 200) & (b > 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(git.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("git", "Git", sp, 372 + ox, 58 + oy)

    # 18. Redis
    c = img[80:150, 424:488].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    redis = (r > 140) & (r > b + 50)
    redis |= (r > 200) & (g > 200) & (b > 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(redis.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("redis", "Redis", sp, 424 + ox, 80 + oy)

    # 19. GoLand (Rotated JetBrains IDE badge)
    c = img[42:118, 480:548].copy()
    ch, cw = c.shape[:2]
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    non_bg = ~is_cosmic_bg(b, g, r)
    non_bg[62:, :] = False
    non_bg[:, :8] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dil = cv2.dilate(non_bg.astype(np.uint8), kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros((ch, cw), dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 400:
            hull = cv2.convexHull(cnt)
            cv2.drawContours(mask, [hull], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("goland", "Go IDE", sp, 480 + ox, 42 + oy)

    # 20. MDN Silver Shield
    c = img[45:105, 545:605].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    mdn = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    mdn[:15, :20] = 0
    mdn[:, 50:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mdn, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("mdn", "MDN Web Docs", sp, 545 + ox, 45 + oy)

    # 21. Vim
    c = img[114:174, 546:604].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    vim = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    vim[:, 46:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(vim, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("vim", "Vim", sp, 546 + ox, 114 + oy)

    # 22. Nginx
    c = img[40:158, 580:670].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    nginx = (g > 115) & (g > r + 25) & (g > b + 25)
    nginx[:, :16] = False
    nginx[85:, :45] = False
    nginx[:15, :] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(nginx.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("nginx", "Nginx", sp, 580 + ox, 40 + oy)

    # 23. Sketch
    c = img[82:142, 630:682].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    sketch = (r > 160) & (g > 120) & (b < 80)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(sketch.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("sketch", "Sketch", sp, 630 + ox, 82 + oy)

    # 24. Apache Kafka
    c = img[30:95, 690:804].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    kf_fg = ~is_cosmic_bg(b, g, r)
    react = (b > 130) & (g > 110) & (r < 100)
    kf_fg[react] = False
    kf_fg[:16, :] = False
    kf_fg[48:, :20] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(kf_fg.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("kafka", "Apache Kafka", sp, 690 + ox, 30 + oy)

    # 25. Kubernetes
    c = img[26:95, 810:878].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    k8s = (b > 125) & (b > r + 25)
    k8s |= (r > 175) & (g > 175) & (b > 175)
    k8s[45:, :24] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dil = cv2.dilate(k8s.astype(np.uint8) * 255, kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 800:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("kubernetes", "Kubernetes", sp, 810 + ox, 26 + oy)

    # 26. Stacked Mini Gophers (Yellow on Purple)
    c = img[50:128, 792:834].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    mg = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mg, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("gopher_pair", "Mini Gophers Pair", sp, 792 + ox, 50 + oy)

    # 27. Pink Mini Gopher with Glasses
    c = img[75:128, 855:895].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    pink = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(pink, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("gopher_pink", "Pink Mini Gopher", sp, 855 + ox, 75 + oy)

    # ================= BOTTOM ROW =================
    # 28. Spring Network Dots
    c = img[162:204, 102:160].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    dots = (b > 120) & (g > 100)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(dots.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("spring_dots", "Spring Network", sp, 102 + ox, 162 + oy)

    # 29. Fortran 3D F
    c = img[110:182, 116:176].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    f_logo = (r > 140) & (g > 70) & (b < 80)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(f_logo.astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, closed)
    register("fortran_f", "Fortran 3D F", sp, 116 + ox, 110 + oy)

    # 30. Blue Hyperledger Cube
    c = img[144:204, 166:238].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    cube = (b > 140) & (b > r + 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(cube.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("blue_cube", "Hyperledger Cube", sp, 166 + ox, 144 + oy)

    # 31. Apple
    c = img[145:204, 250:312].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    apple = (r > 90) & (g > 90) & (b > 90) & (abs(r.astype(int) - g.astype(int)) < 25) & ~is_cosmic_bg(b, g, r)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dil = cv2.dilate(apple.astype(np.uint8) * 255, kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 400:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("apple", "Apple", sp, 250 + ox, 145 + oy)

    # 32. Blue Chevrons
    c = img[112:165, 306:352].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    chev = (b > 130) & (b > r + 20)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(chev.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("blue_chevrons", "Blue Chevrons", sp, 306 + ox, 112 + oy)

    # 33. GitLab
    c = img[116:176, 345:395].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    fox = (r > 150) & (r > b + 50)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(fox.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("gitlab", "GitLab", sp, 345 + ox, 116 + oy)

    # 34. Wireshark Fin
    c = img[165:204, 320:374].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    fin = (b > 120) & (b > r + 30)
    fin |= (r > 180) & (g > 180) & (b > 180)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(fin.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("wireshark_fin", "Wireshark Fin", sp, 320 + ox, 165 + oy)

    # 35. JavaScript
    c = img[136:188, 392:444].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    js = (r > 170) & (g > 150) & (b < 100)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dil = cv2.dilate(js.astype(np.uint8) * 255, kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 400:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("javascript", "JavaScript", sp, 392 + ox, 136 + oy)

    # 36. HTML5 Badge
    c = img[155:204, 408:456].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    html5 = (r > 150) & (r > b + 45)
    html5 |= (r > 180) & (g > 180) & (b > 180)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(html5.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("html5_badge", "HTML5 Shield", sp, 408 + ox, 155 + oy)

    # 37. Go Gopher Mascot
    c = img[102:204, 450:558].copy()
    gh, gw = c.shape[:2]
    b, g, r = c[:, :, 0].astype(int), c[:, :, 1].astype(int), c[:, :, 2].astype(int)
    gopher_seed = ((b > 120) & (g > 100)) & ~((r > 160) & (g > 160) & (b < 100))
    gopher_seed[:, :16] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    gopher_dil = cv2.dilate(gopher_seed.astype(np.uint8), kernel)
    contours, _ = cv2.findContours(gopher_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros((gh, gw), dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 1500:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("gopher_mascot", "Go Gopher Mascot", sp, 450 + ox, 102 + oy)

    # 38. Jenkins Butler Face & Bowtie
    c = img[116:185, 570:645].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    dist = np.sqrt((b.astype(float) - 40.0)**2 + (g.astype(float) - 9.0)**2 + (r.astype(float) - 4.0)**2)
    bg = (dist < 26) | ((b < 50) & (g < 22) & (r < 20))
    bg |= (g > 120) & (g > r + 30) & (g > b + 30)
    fg = ~bg
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 600:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("jenkins", "Jenkins", sp, 570 + ox, 116 + oy)

    # 39. Jenkins Gear Badge
    c = img[165:204, 550:595].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    gear = (~is_cosmic_bg(b, g, r)).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(gear, cv2.MORPH_CLOSE, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("jenkins_gear", "Jenkins Gear", sp, 550 + ox, 165 + oy)

    # 40. Red Speed Streaks
    c = img[175:204, 615:675].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    streaks = (r > 130) & (r > b + 40)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(streaks.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("red_streaks", "Speed Streaks", sp, 615 + ox, 175 + oy)

    # 41. PostgreSQL Elephant
    c = img[90:195, 655:745].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    elephant = (b > 105) & (b > r + 25)
    elephant |= (r > 175) & (g > 175) & (b > 175)
    elephant[:12, :] = False
    elephant[:, :8] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dil = cv2.dilate(elephant.astype(np.uint8) * 255, kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 1000:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("postgres", "PostgreSQL", sp, 655 + ox, 90 + oy)

    # 42. RabbitMQ Orange Rabbit Head
    c = img[70:145, 736:806].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    rmq = (r > 170) & (g > 65) & (g < 145) & (b < 65)
    rmq |= (r > 180) & (g > 180) & (b > 180) & (c.shape[1] - np.arange(c.shape[1])[None, :] > 20)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dil = cv2.dilate(rmq.astype(np.uint8), kernel)
    contours, _ = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(c.shape[:2], dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 400:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("rabbitmq", "RabbitMQ", sp, 736 + ox, 70 + oy)

    # 43. MySQL Dolphin & Logo
    c = img[110:204, 680:800].copy()
    b, g, r = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    mysql = (r > 150) & (g > 90)
    mysql |= (b > 110) & (g > 65)
    mysql[:50, :45] = False
    mysql[:35, 60:] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(mysql.astype(np.uint8) * 255, kernel)
    sp, ox, oy = create_sprite(c, mask)
    register("mysql", "MySQL", sp, 680 + ox, 110 + oy)

    # 44. Xcode App Store + Hammer
    c = img[108:204, 792:905].copy()
    xh, xw = c.shape[:2]
    b, g, r = c[:, :, 0].astype(int), c[:, :, 1].astype(int), c[:, :, 2].astype(int)
    bg = is_cosmic_bg(b, g, r)
    xcode_seed = (~bg) & (np.arange(xw)[None, :] > 8)
    xcode_seed[:24, :40] = False
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    xcode_dil = cv2.dilate(xcode_seed.astype(np.uint8), kernel)
    contours, _ = cv2.findContours(xcode_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros((xh, xw), dtype=np.uint8)
    for cnt in contours:
        if cv2.contourArea(cnt) > 3000:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    sp, ox, oy = create_sprite(c, mask)
    register("xcode_appstore", "App Store / Xcode", sp, 792 + ox, 108 + oy)

    print(f"Total extracted authentic icons: {len(extracted_results)}")
    
    meta_payload = {
        "bannerWidth": 1024,
        "bannerHeight": 204,
        "icons": extracted_results
    }
    
    with open("assets/icons-metadata.json", "w") as f:
        json.dump(meta_payload, f, indent=2)
    with open("docs/assets/icons-metadata.json", "w") as f:
        json.dump(meta_payload, f, indent=2)
    print("Saved metadata dictionary to assets/ and docs/assets/")

extract_all()
