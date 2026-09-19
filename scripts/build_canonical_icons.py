import os
import urllib.request
import json
import fitz  # PyMuPDF
from PIL import Image

ASSETS_ICONS_DIR = "/Users/nguyenvanminhtam/nvmtamm/assets/interactive-icons"
DOCS_ICONS_DIR = "/Users/nguyenvanminhtam/nvmtamm/docs/assets/icons"
CACHE_DIR = "/Users/nguyenvanminhtam/nvmtamm/scripts/svg_cache"

os.makedirs(ASSETS_ICONS_DIR, exist_ok=True)
os.makedirs(DOCS_ICONS_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

DEVICON = "https://raw.githubusercontent.com/devicons/devicon/master/icons/"
SIMPLE = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/"

# 37 canonical icons with EXACT calibrated bounding box sizes & centers from original-footer.png
CALIBRATED_ICONS = [
    # --- TOP ROW ---
    {
        "id": "gulp", "name": "Gulp",
        "url": DEVICON + "gulp/gulp-plain.svg",
        "origX": 140, "origY": 48, "w": 40, "h": 60, "z": 1
    },
    {
        "id": "cinema4d", "name": "Cinema 4D",
        "origX": 206, "origY": 53, "w": 76, "h": 86, "z": 1,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120">
            <polygon points="68,10 86,10 18,74 0,74" fill="#00A2FF"/>
            <polygon points="0,74 18,74 96,74 96,56 18,56" fill="#0084FF"/>
            <polygon points="18,56 34,42 42,48 26,62" fill="#0066CC"/>
            <polygon points="60,18 78,18 78,110 60,110" fill="#0072E3"/>
            <polygon points="73,18 78,18 78,110 73,110" fill="#0057B8"/>
        </svg>"""
    },
    {
        "id": "debian", "name": "Debian Sun Swirl",
        "origX": 278, "origY": 48, "w": 64, "h": 72, "z": 1,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
            <path fill="#FF7700" d="M64 4 L74 20 L94 14 L94 34 L114 38 L104 56 L124 64 L104 72 L114 90 L94 94 L94 114 L74 108 L64 124 L54 108 L34 114 L34 94 L14 90 L24 72 L4 64 L24 56 L14 38 L34 34 L34 14 L54 20 Z"/>
            <circle cx="64" cy="64" r="42" fill="#FFA000"/>
            <circle cx="64" cy="64" r="34" fill="#FFB300"/>
            <path fill="#18181B" d="M68 34 C82 36 94 48 94 64 C94 80 80 94 64 94 C48 94 36 82 36 66 C36 54 44 44 54 40 C62 37 70 40 74 46 C78 52 76 60 70 64 C64 68 56 66 54 60 C52 56 54 52 58 50 C60 49 61 51 60 52 C57 54 56 57 58 60 C60 63 64 64 68 62 C72 60 74 54 71 50 C68 46 62 44 56 46 C48 49 42 57 42 66 C42 78 52 88 64 88 C76 88 88 78 88 64 C88 52 78 42 66 40 C58 39 50 42 46 48 C45 49 43 48 44 46 C49 39 58 35 68 34 Z"/>
        </svg>"""
    },
    {
        "id": "grpc", "name": "gRPC",
        "origX": 380, "origY": 32, "w": 120, "h": 40, "z": 1,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 70">
            <path d="M12 25 L24 12 L24 20 L38 20 L38 30 L24 30 L24 38 Z" fill="#00E5FF"/>
            <path d="M52 25 L40 12 L40 20 L26 20 L26 30 L40 30 L40 38 Z" fill="#00E5FF"/>
            <line x1="22" y1="25" x2="42" y2="25" stroke="#FFFFFF" stroke-width="3"/>
            <text x="56" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
                  font-size="44" font-weight="700" fill="#FFFFFF" letter-spacing="1">gRPC</text>
        </svg>"""
    },
    {
        "id": "photoshop", "name": "Adobe Photoshop",
        "origX": 467, "origY": 52, "w": 42, "h": 48, "z": 1,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <rect x="4" y="4" width="92" height="92" rx="18" fill="#001E36" stroke="#31A8FF" stroke-width="6"/>
            <text x="24" y="68" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="48" font-weight="700" fill="#31A8FF">Ps</text>
        </svg>"""
    },
    {
        "id": "npm", "name": "npm Package Manager",
        "url": DEVICON + "npm/npm-original-wordmark.svg",
        "origX": 534, "origY": 35, "w": 56, "h": 38, "z": 1
    },
    {
        "id": "go_speed", "name": "Go (Fast Engine)",
        "url": DEVICON + "go/go-original-wordmark.svg",
        "origX": 605, "origY": 42, "w": 74, "h": 52, "z": 1
    },
    {
        "id": "probot", "name": "Probot GitHub App",
        "origX": 672, "origY": 55, "w": 44, "h": 54, "z": 1,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <polygon points="25,15 75,15 90,45 80,85 20,85 10,45" fill="#E2E8F0" stroke="#94A3B8" stroke-width="3"/>
            <rect x="25" y="38" width="18" height="24" rx="4" fill="#00E5FF"/>
            <rect x="57" y="38" width="18" height="24" rx="4" fill="#00E5FF"/>
            <rect x="35" y="72" width="30" height="6" rx="2" fill="#475569"/>
        </svg>"""
    },
    {
        "id": "react", "name": "React.js",
        "url": DEVICON + "react/react-original.svg",
        "origX": 722, "origY": 56, "w": 56, "h": 60, "z": 1
    },
    {
        "id": "elastic", "name": "Elasticsearch",
        "url": DEVICON + "elasticsearch/elasticsearch-original.svg",
        "origX": 779, "origY": 57, "w": 50, "h": 54, "z": 1
    },
    {
        "id": "illustrator", "name": "Adobe Illustrator",
        "origX": 830, "origY": 52, "w": 44, "h": 48, "z": 1,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <rect x="4" y="4" width="92" height="92" rx="18" fill="#331A00" stroke="#FF9A00" stroke-width="6"/>
            <text x="26" y="68" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="48" font-weight="700" fill="#FF9A00">Ai</text>
        </svg>"""
    },
    {
        "id": "eagle_bird", "name": "Blue Eagle / Speed",
        "origX": 885, "origY": 54, "w": 58, "h": 64, "z": 1,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <path fill="#00B4D8" d="M50 8 C30 8 12 28 15 53 C16 61 20 70 25 74 C23 66 25 58 30 53 C35 48 42 46 48 43 C40 48 36 58 38 68 C40 76 47 82 55 84 C50 80 48 74 50 68 C53 62 60 58 67 58 C62 63 60 70 63 76 C65 80 70 83 76 82 C73 78 73 73 76 69 C80 65 88 64 94 68 C92 53 90 38 80 26 C72 16 62 8 50 8 Z"/>
            <circle cx="75" cy="38" r="5" fill="#ffffff"/>
            <circle cx="76.5" cy="38" r="2.5" fill="#0b1329"/>
            <path fill="#FFB703" d="M84 43 C91 46 96 51 98 58 C92 55 88 52 83 49 Z"/>
        </svg>"""
    },

    # --- MIDDLE ROW ---
    {
        "id": "swift", "name": "Apple Swift",
        "url": DEVICON + "swift/swift-original.svg",
        "origX": 122, "origY": 127, "w": 64, "h": 62, "z": 2
    },
    {
        "id": "bracket_e", "name": "Hex Code <e/>",
        "origX": 186, "origY": 135, "w": 56, "h": 46, "z": 2,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80">
            <defs>
                <linearGradient id="hexGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00E5FF"/>
                    <stop offset="100%" stop-color="#0088FF"/>
                </linearGradient>
            </defs>
            <path stroke="url(#hexGrad)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"
                  d="M32 20 L15 40 L32 60 M68 20 L85 40 L68 60"/>
            <path fill="url(#hexGrad)" d="M50 25 C41 25 35 31 35 40 C35 49 41 55 50 55 C56 55 61 52 63 47 L55 47 C54 49 52 50 50 50 C45 50 42 46 42 42 L64 42 C64 41 64 40 64 39 C64 30 58 25 50 25 Z M42 38 C43 34 45 30 50 30 C54 30 57 34 57 38 L42 38 Z"/>
        </svg>"""
    },
    {
        "id": "github", "name": "GitHub Octocat",
        "origX": 247, "origY": 147, "w": 58, "h": 58, "z": 2,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="48" fill="#FFFFFF"/>
            <path fill="#181717" d="M50 15 C30.67 15 15 30.67 15 50 C15 65.47 25.03 78.58 38.98 83.22 C40.73 83.54 41.37 82.46 41.37 81.53 C41.37 80.71 41.34 78.53 41.32 75.66 C31.59 77.77 29.53 71.49 29.53 71.49 C27.94 67.44 25.64 66.36 25.64 66.36 C22.46 64.19 25.88 64.23 25.88 64.23 C29.4 64.48 31.25 68.09 31.25 68.09 C34.37 73.44 39.45 71.89 41.45 70.99 C41.77 68.73 42.67 67.18 43.67 66.31 C35.9 65.42 27.73 62.43 27.73 49.03 C27.73 45.21 29.09 42.08 31.33 39.63 C30.97 38.74 29.77 35.19 31.68 30.38 C31.68 30.38 34.61 29.44 41.27 33.94 C44.06 33.16 47.04 32.77 50.01 32.76 C52.98 32.77 55.97 33.16 58.76 33.94 C65.41 29.44 68.33 30.38 68.33 30.38 C70.25 35.19 69.05 38.74 68.69 39.63 C70.94 42.08 72.28 45.21 72.28 49.03 C72.28 62.47 64.09 65.41 56.28 66.28 C57.53 67.36 58.64 69.49 58.64 72.76 C58.64 77.45 58.6 81.24 58.6 82.38 C58.6 83.33 59.23 84.43 61.02 84.08 C74.96 79.43 85 66.32 85 50 C85 30.67 69.33 15 50 15 Z"/>
        </svg>"""
    },
    {
        "id": "docker", "name": "Docker Engine",
        "url": DEVICON + "docker/docker-original.svg",
        "origX": 332, "origY": 112, "w": 96, "h": 72, "z": 2
    },
    {
        "id": "git", "name": "Git VCS",
        "url": DEVICON + "git/git-original.svg",
        "origX": 406, "origY": 85, "w": 48, "h": 50, "z": 2
    },
    {
        "id": "redis", "name": "Redis In-Memory DB",
        "url": DEVICON + "redis/redis-original.svg",
        "origX": 454, "origY": 113, "w": 52, "h": 54, "z": 2
    },
    {
        "id": "goland", "name": "JetBrains GoLand",
        "url": DEVICON + "goland/goland-original.svg",
        "origX": 516, "origY": 97, "w": 56, "h": 58, "z": 2
    },
    {
        "id": "nginx", "name": "NGINX Web Server",
        "url": DEVICON + "nginx/nginx-original.svg",
        "origX": 614, "origY": 147, "w": 56, "h": 70, "z": 2
    },
    {
        "id": "sketch", "name": "Sketch UI Design",
        "url": DEVICON + "sketch/sketch-original.svg",
        "origX": 663, "origY": 121, "w": 54, "h": 54, "z": 2
    },
    {
        "id": "kafka", "name": "Apache Kafka",
        "url": DEVICON + "apachekafka/apachekafka-original-wordmark.svg",
        "color_transform": {"#231F20": "#FFFFFF", "#000000": "#FFFFFF", "#000": "#FFFFFF"},
        "origX": 740, "origY": 125, "w": 90, "h": 50, "z": 2
    },
    {
        "id": "kubernetes", "name": "Kubernetes (K8s)",
        "url": DEVICON + "kubernetes/kubernetes-plain.svg",
        "color": "#326CE5",
        "origX": 840, "origY": 129, "w": 56, "h": 58, "z": 2
    },
    {
        "id": "xcode_appstore", "name": "Apple Xcode",
        "url": DEVICON + "xcode/xcode-plain.svg",
        "origX": 891, "origY": 154, "w": 78, "h": 84, "z": 2
    },

    # --- BOTTOM ROW ---
    {
        "id": "spring_dots", "name": "Cardano Network",
        "url": SIMPLE + "cardano.svg",
        "color": "#00E5FF",
        "origX": 129, "origY": 182, "w": 46, "h": 40, "z": 3
    },
    {
        "id": "fortran_f", "name": "Fortran 3D / F#",
        "url": DEVICON + "fortran/fortran-original.svg",
        "origX": 149, "origY": 168, "w": 46, "h": 52, "z": 3
    },
    {
        "id": "blue_cube", "name": "Hyperledger / Web3 Cube",
        "origX": 201, "origY": 178, "w": 62, "h": 48, "z": 3,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 90">
            <polygon points="50,5 88,27 88,71 50,93 12,71 12,27" stroke="#00E5FF" stroke-width="4" fill="none"/>
            <polygon points="50,22 76,36 50,50 24,36" fill="#40C4FF"/>
            <polygon points="24,36 50,50 50,78 24,64" fill="#0091EA"/>
            <polygon points="50,50 76,36 76,64 50,78" fill="#0277BD"/>
        </svg>"""
    },
    {
        "id": "apple", "name": "Apple Ecosystem",
        "url": DEVICON + "apple/apple-original.svg",
        "color": "#F1F5F9",
        "origX": 276, "origY": 184, "w": 56, "h": 36, "z": 3
    },
    {
        "id": "wireshark_fin", "name": "Wireshark Packet Analysis",
        "origX": 342, "origY": 188, "w": 46, "h": 28, "z": 3,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80">
            <path d="M10 70 C35 70, 75 55, 90 10 C80 35, 65 60, 40 68 Z" fill="#00A3E0"/>
            <path d="M5 72 Q25 65 50 72 T95 72" stroke="#FFFFFF" stroke-width="4" fill="none"/>
        </svg>"""
    },
    {
        "id": "gitlab", "name": "GitLab CI/CD",
        "url": DEVICON + "gitlab/gitlab-original.svg",
        "origX": 369, "origY": 186, "w": 42, "h": 32, "z": 3
    },
    {
        "id": "javascript", "name": "JavaScript (ES6+)",
        "origX": 415, "origY": 181, "w": 42, "h": 42, "z": 3,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
            <rect fill="#F7DF1E" x="4" y="4" width="120" height="120" rx="22" ry="22"/>
            <path fill="#000000" d="M116.347 96.736c-.917-5.711-4.641-10.508-15.672-14.981-3.832-1.761-8.104-3.022-9.377-5.926-.452-1.69-.512-2.642-.226-3.665.821-3.32 4.784-4.355 7.925-3.403 2.023.678 3.938 2.237 5.093 4.724 5.402-3.498 5.391-3.475 9.163-5.879-1.381-2.141-2.118-3.129-3.022-4.045-3.249-3.629-7.676-5.498-14.756-5.355l-3.688.477c-3.534.893-6.902 2.748-8.877 5.235-5.926 6.724-4.236 18.492 2.975 23.335 7.104 5.332 17.54 6.545 18.873 11.531 1.297 6.104-4.486 8.08-10.234 7.378-4.236-.881-6.592-3.034-9.139-6.949-4.688 2.713-4.688 2.713-9.508 5.485 1.143 2.499 2.344 3.63 4.26 5.795 9.068 9.198 31.76 8.746 35.83-5.176.165-.478 1.261-3.666.38-8.581zM69.462 58.943H57.753l-.048 30.272c0 6.438.333 12.34-.714 14.149-1.713 3.558-6.152 3.117-8.175 2.427-2.059-1.012-3.106-2.451-4.319-4.485-.333-.584-.583-1.036-.667-1.071l-9.52 5.83c1.583 3.249 3.915 6.069 6.902 7.901 4.462 2.678 10.459 3.499 16.731 2.059 4.082-1.189 7.604-3.652 9.448-7.401 2.666-4.915 2.094-10.864 2.07-17.444.06-10.735.001-21.468.001-32.237z"/>
        </svg>"""
    },
    {
        "id": "html5_badge", "name": "HTML5 Web Standard",
        "url": DEVICON + "html5/html5-original.svg",
        "origX": 434, "origY": 191, "w": 36, "h": 22, "z": 3
    },
    {
        "id": "jenkins", "name": "Jenkins CI/CD",
        "url": DEVICON + "jenkins/jenkins-original.svg",
        "origX": 605, "origY": 180, "w": 46, "h": 44, "z": 3
    },
    {
        "id": "postgres", "name": "PostgreSQL Database",
        "url": DEVICON + "postgresql/postgresql-original.svg",
        "origX": 699, "origY": 171, "w": 70, "h": 62, "z": 3
    },
    {
        "id": "mysql", "name": "MySQL Database",
        "url": DEVICON + "mysql/mysql-original-wordmark.svg",
        "origX": 774, "origY": 182, "w": 68, "h": 40, "z": 3
    },
    {
        "id": "gopher_pair", "name": "Mini Companion Gophers",
        "origX": 851, "origY": 180, "w": 58, "h": 44, "z": 3,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 100">
            <ellipse cx="35" cy="55" rx="20" ry="26" fill="#F4D03F" stroke="#000" stroke-width="3"/>
            <circle cx="28" cy="45" r="9" fill="#FFF" stroke="#000" stroke-width="2.5"/>
            <circle cx="44" cy="45" r="9" fill="#FFF" stroke="#000" stroke-width="2.5"/>
            <circle cx="28" cy="45" r="3.5" fill="#000"/>
            <circle cx="44" cy="45" r="3.5" fill="#000"/>
            <ellipse cx="36" cy="56" rx="6" ry="4" fill="#E59866" stroke="#000" stroke-width="1.5"/>
            <ellipse cx="85" cy="58" rx="20" ry="25" fill="#F1948A" stroke="#000" stroke-width="3"/>
            <circle cx="78" cy="48" r="9" fill="#FFF" stroke="#000" stroke-width="2.5"/>
            <circle cx="94" cy="48" r="9" fill="#FFF" stroke="#000" stroke-width="2.5"/>
            <circle cx="78" cy="48" r="3.5" fill="#000"/>
            <circle cx="94" cy="48" r="3.5" fill="#000"/>
            <ellipse cx="86" cy="59" rx="6" ry="4" fill="#E59866" stroke="#000" stroke-width="1.5"/>
        </svg>"""
    },

    # --- FOREGROUND CENTERPIECE ---
    {
        "id": "gopher_mascot", "name": "Go Gopher Mascot (Full)",
        "origX": 497, "origY": 170, "w": 78, "h": 64, "z": 4,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 310">
            <defs>
                <radialGradient id="earInner" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#000000"/>
                    <stop offset="100%" stop-color="#111111"/>
                </radialGradient>
            </defs>
            <ellipse cx="40" cy="55" rx="30" ry="26" fill="#6ad7e5" stroke="#000000" stroke-width="8"/>
            <circle cx="42" cy="55" r="14" fill="url(#earInner)"/>
            <ellipse cx="210" cy="55" rx="30" ry="26" fill="#6ad7e5" stroke="#000000" stroke-width="8"/>
            <circle cx="208" cy="55" r="14" fill="url(#earInner)"/>
            <path d="M 45 80 C 45 40, 205 40, 205 80 C 210 130, 215 220, 200 270 C 185 305, 65 305, 50 270 C 35 220, 40 130, 45 80 Z"
                  fill="#6ad7e5" stroke="#000000" stroke-width="9" stroke-linejoin="round"/>
            <ellipse cx="22" cy="170" rx="14" ry="12" fill="#e0bb8b" stroke="#000000" stroke-width="6"/>
            <ellipse cx="228" cy="170" rx="14" ry="12" fill="#e0bb8b" stroke="#000000" stroke-width="6"/>
            <ellipse cx="70" cy="295" rx="20" ry="14" fill="#e0bb8b" stroke="#000000" stroke-width="6"/>
            <ellipse cx="180" cy="295" rx="20" ry="14" fill="#e0bb8b" stroke="#000000" stroke-width="6"/>
            <ellipse cx="82" cy="85" rx="36" ry="40" fill="#ffffff" stroke="#000000" stroke-width="8"/>
            <circle cx="68" cy="78" r="13" fill="#000000"/>
            <circle cx="64" cy="74" r="4.5" fill="#ffffff"/>
            <ellipse cx="160" cy="85" rx="36" ry="40" fill="#ffffff" stroke="#000000" stroke-width="8"/>
            <circle cx="146" cy="78" r="13" fill="#000000"/>
            <circle cx="142" cy="74" r="4.5" fill="#ffffff"/>
            <ellipse cx="120" cy="120" rx="25" ry="18" fill="#e0bb8b" stroke="#000000" stroke-width="6"/>
            <ellipse cx="120" cy="110" rx="14" ry="10" fill="#000000"/>
            <path d="M 111 134 L 111 150 C 111 153, 119 153, 119 150 L 119 134 Z" fill="#ffffff" stroke="#000000" stroke-width="4.5"/>
            <path d="M 121 134 L 121 150 C 121 153, 129 153, 129 150 L 129 134 Z" fill="#ffffff" stroke="#000000" stroke-width="4.5"/>
            <polygon points="98,168 116,176 98,184" fill="#1c2536" stroke="#000000" stroke-width="3"/>
            <polygon points="142,168 124,176 142,184" fill="#1c2536" stroke="#000000" stroke-width="3"/>
            <ellipse cx="120" cy="176" rx="6" ry="7" fill="#ffffff" stroke="#000000" stroke-width="3"/>
        </svg>"""
    }
]

def fetch_or_get_svg(item):
    svg_file = os.path.join(CACHE_DIR, f"{item['id']}.svg")
    
    if "svg" in item:
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(item["svg"])
        return svg_file
        
    url = item["url"]
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
        
    if "color_transform" in item:
        for old_c, new_c in item["color_transform"].items():
            content = content.replace(f'fill="{old_c}"', f'fill="{new_c}"')
            content = content.replace(f'stroke="{old_c}"', f'stroke="{new_c}"')
            
    if "color" in item:
        color = item["color"]
        content = content.replace('fill="#000000"', f'fill="{color}"')
        content = content.replace('fill="#000"', f'fill="{color}"')
        content = content.replace('fill="currentColor"', f'fill="{color}"')
        if 'fill=' not in content:
            content = content.replace('<path ', f'<path fill="{color}" ')
            
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    return svg_file

def render_svg_to_png(svg_path, out_png_path1, out_png_path2, target_w, target_h):
    doc = fitz.open(svg_path)
    page = doc[0]
    
    scale = max(2.5, 200.0 / max(page.rect.width, page.rect.height))
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    
    img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
    
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    # Render at 2x for Retina crispness
    render_w = int(target_w * 2)
    render_h = int(target_h * 2)
    img_resized = img.resize((render_w, render_h), Image.Resampling.LANCZOS)
    
    img_resized.save(out_png_path1, format="PNG")
    img_resized.save(out_png_path2, format="PNG")

metadata_list = []
banner_w = 1024
banner_h = 204

for item in CALIBRATED_ICONS:
    svg_path = fetch_or_get_svg(item)
    png_path1 = os.path.join(ASSETS_ICONS_DIR, f"{item['id']}.png")
    png_path2 = os.path.join(DOCS_ICONS_DIR, f"{item['id']}.png")
    
    target_w = item["w"]
    target_h = item["h"]
    
    render_svg_to_png(svg_path, png_path1, png_path2, target_w, target_h)
    
    orig_x = item["origX"]
    orig_y = item["origY"]
    radius = int(max(target_w, target_h) / 2)
    
    meta_entry = {
        "id": item["id"],
        "name": item["name"],
        "src": f"assets/icons/{item['id']}.png",
        "width": int(target_w),
        "height": int(target_h),
        "radius": radius,
        "origX": float(orig_x),
        "origY": float(orig_y),
        "normX": float(orig_x / banner_w),
        "normY": float(orig_y / banner_h),
        "zIndex": item.get("z", 1)
    }
    metadata_list.append(meta_entry)

meta_data = {
    "bannerWidth": banner_w,
    "bannerHeight": banner_h,
    "totalIcons": len(metadata_list),
    "icons": metadata_list
}

with open("/Users/nguyenvanminhtam/nvmtamm/assets/icons-metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta_data, f, indent=2, ensure_ascii=False)

with open("/Users/nguyenvanminhtam/nvmtamm/docs/assets/icons-metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta_data, f, indent=2, ensure_ascii=False)

print(f"\nSUCCESS! All {len(metadata_list)} icons calibrated and updated.")
