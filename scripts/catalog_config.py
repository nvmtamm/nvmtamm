import cv2
import json
import numpy as np
import os

img = cv2.imread("/Users/nguyenvanminhtam/nvmtamm/assets/original-footer.png")
h, w = img.shape[:2]

# Full catalog of all icons in the image
ICONS_CATALOG = [
    # Top Row
    {"name": "gulp", "title": "Gulp", "rect": (118, 12, 172, 85)},
    {"name": "cinema4d", "title": "Cinema 4D", "rect": (168, 8, 246, 105)},
    {"name": "debian", "title": "Debian / Grafana", "rect": (245, 5, 315, 88)},
    {"name": "grpc", "title": "gRPC", "rect": (318, 10, 442, 80)},
    {"name": "photoshop", "title": "Photoshop", "rect": (444, 25, 492, 85)},
    {"name": "npm", "title": "npm", "rect": (504, 15, 565, 72)},
    {"name": "go_speed", "title": "Go Lang", "rect": (565, 14, 646, 82)},
    {"name": "probot", "title": "Probot", "rect": (645, 28, 694, 85)},
    {"name": "react", "title": "React", "rect": (690, 24, 752, 96)},
    {"name": "elastic", "title": "Elasticsearch", "rect": (752, 32, 806, 96)},
    {"name": "illustrator", "title": "Illustrator", "rect": (806, 28, 856, 88)},
    {"name": "eagle_bird", "title": "Blue Eagle", "rect": (856, 22, 920, 95)},

    # Middle Row
    {"name": "swift", "title": "Swift", "rect": (96, 96, 162, 162)},
    {"name": "bracket_e", "title": "Hex Code", "rect": (165, 108, 224, 162)},
    {"name": "github", "title": "GitHub", "rect": (224, 115, 284, 180)},
    {"name": "docker", "title": "Docker", "rect": (280, 68, 382, 155)},
    {"name": "git", "title": "Git", "rect": (376, 94, 432, 155)},
    {"name": "redis", "title": "Redis", "rect": (422, 115, 474, 180)},
    {"name": "goland", "title": "Go IDE", "rect": (478, 92, 536, 160)},
    {"name": "nginx", "title": "Nginx", "rect": (585, 112, 642, 186)},
    {"name": "sketch", "title": "Sketch", "rect": (632, 94, 694, 155)},
    {"name": "kafka", "title": "Apache Kafka", "rect": (692, 106, 786, 158)},
    {"name": "kubernetes", "title": "Kubernetes", "rect": (806, 100, 866, 165)},
    {"name": "xcode_appstore", "title": "App Store / Xcode", "rect": (850, 110, 930, 204)},

    # Bottom Row
    {"name": "spring_dots", "title": "Spring Network", "rect": (104, 168, 158, 204)},
    {"name": "fortran_f", "title": "Fortran / 3D F", "rect": (126, 142, 178, 204)},
    {"name": "blue_cube", "title": "Hyperledger / Web3 Cube", "rect": (168, 152, 235, 204)},
    {"name": "apple", "title": "Apple", "rect": (248, 166, 310, 204)},
    {"name": "wireshark_fin", "title": "Wireshark Fin", "rect": (312, 172, 368, 204)},
    {"name": "gitlab", "title": "GitLab", "rect": (346, 170, 396, 204)},
    {"name": "javascript", "title": "JavaScript", "rect": (388, 162, 436, 204)},
    {"name": "html5_badge", "title": "HTML5 Shield", "rect": (408, 182, 452, 204)},
    {"name": "gopher_mascot", "title": "Go Gopher Mascot", "rect": (440, 142, 542, 204)},
    {"name": "jenkins", "title": "Jenkins", "rect": (574, 158, 626, 204)},
    {"name": "postgres", "title": "PostgreSQL", "rect": (658, 136, 735, 204)},
    {"name": "mysql", "title": "MySQL", "rect": (730, 162, 808, 204)},
    {"name": "gopher_pair", "title": "Cute Mini Gophers", "rect": (820, 156, 882, 204)}
]

print(f"Total defined icons: {len(ICONS_CATALOG)}")
