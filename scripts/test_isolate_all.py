import cv2
import numpy as np
import os
import json

img = cv2.imread("assets/original-footer.png")
H, W, _ = img.shape

# Precise manual bounding boxes for inspection
ICONS_RAW = [
    # Top Row
    {"id": "gulp", "name": "Gulp", "box": (115, 12, 168, 86)},
    {"id": "cinema4d", "name": "Cinema 4D", "box": (160, 8, 248, 105)},
    {"id": "debian", "name": "Debian / Grafana", "box": (242, 5, 318, 92)},
    {"id": "grpc", "name": "gRPC", "box": (316, 8, 442, 60)},
    {"id": "photoshop", "name": "Photoshop", "box": (444, 25, 495, 76)},
    {"id": "npm", "name": "npm", "box": (504, 10, 568, 50)},
    {"id": "go_speed", "name": "Go Lang Speed", "box": (567, 13, 649, 66)},
    {"id": "probot", "name": "Probot", "box": (648, 27, 697, 80)},
    {"id": "react", "name": "React", "box": (693, 22, 752, 82)},
    {"id": "elastic", "name": "Elasticsearch", "box": (751, 26, 805, 83)},
    {"id": "illustrator", "name": "Illustrator", "box": (804, 23, 848, 70)},
    {"id": "eagle_bird", "name": "Blue Eagle", "box": (847, 15, 910, 72)},

    # Mid Row
    {"id": "swift", "name": "Swift", "box": (84, 84, 144, 146)},
    {"id": "bracket_e", "name": "Hex Code <e>", "box": (153, 105, 214, 166)},
    {"id": "github", "name": "GitHub", "box": (222, 86, 282, 146)},
    {"id": "docker", "name": "Docker", "box": (280, 53, 388, 145)},
    {"id": "git", "name": "Git", "box": (377, 68, 434, 125)},
    {"id": "redis", "name": "Redis", "box": (428, 92, 485, 146)},
    {"id": "goland", "name": "Go IDE", "box": (484, 55, 544, 117)},
    {"id": "nginx", "name": "Nginx", "box": (592, 74, 648, 155)},
    {"id": "vim", "name": "Vim", "box": (546, 116, 603, 174)},
    {"id": "sketch", "name": "Sketch", "box": (632, 84, 682, 142)},
    {"id": "kafka", "name": "Apache Kafka", "box": (692, 86, 795, 148)},
    {"id": "kubernetes", "name": "Kubernetes", "box": (810, 83, 870, 144)},

    # Bottom Row
    {"id": "spring_dots", "name": "Spring Network", "box": (104, 162, 160, 204)},
    {"id": "fortran_f", "name": "Fortran 3D F", "box": (120, 130, 172, 190)},
    {"id": "blue_cube", "name": "Hyperledger Cube", "box": (168, 144, 238, 204)},
    {"id": "apple", "name": "Apple", "box": (252, 146, 312, 204)},
    {"id": "blue_brackets", "name": "Blue Chevron", "box": (310, 110, 350, 160)},
    {"id": "wireshark_fin", "name": "Wireshark Fin", "box": (322, 166, 374, 204)},
    {"id": "gitlab", "name": "GitLab", "box": (348, 155, 390, 202)},
    {"id": "javascript", "name": "JavaScript", "box": (394, 138, 444, 188)},
    {"id": "html5_badge", "name": "HTML5 Shield", "box": (416, 178, 452, 204)},
    {"id": "gopher_mascot", "name": "Go Gopher Mascot", "box": (450, 103, 542, 204)},
    {"id": "jenkins", "name": "Jenkins Butler", "box": (570, 142, 630, 204)},
    {"id": "postgres", "name": "PostgreSQL", "box": (662, 125, 740, 194)},
    {"id": "mysql", "name": "MySQL", "box": (732, 148, 796, 204)},
    {"id": "gopher_pair", "name": "Mini Gophers", "box": (798, 136, 868, 176)},
    {"id": "xcode_appstore", "name": "Xcode & Hammer", "box": (792, 108, 905, 204)},
]

out_dir = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/raw_boxes"
os.makedirs(out_dir, exist_ok=True)

for item in ICONS_RAW:
    x1, y1, x2, y2 = item["box"]
    crop = img[y1:y2, x1:x2]
    cv2.imwrite(f"{out_dir}/{item['id']}.png", crop)

print(f"Exported {len(ICONS_RAW)} raw crops to {out_dir}")
