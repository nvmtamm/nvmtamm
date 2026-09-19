import cv2
import numpy as np
import os

img = cv2.imread("assets/original-footer.png")
scratch = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch"

# 1. Go Speed: x: 565..655, y: 12..66
crop_gospeed = img[12:66, 565:655]
cv2.imwrite(f"{scratch}/debug_gospeed.png", crop_gospeed)

# 2. GoLand: x: 480..545, y: 55..120
crop_goland = img[55:120, 480:545]
cv2.imwrite(f"{scratch}/debug_goland.png", crop_goland)

# 3. NGINX: x: 585..655, y: 65..160
crop_nginx = img[65:160, 585:655]
cv2.imwrite(f"{scratch}/debug_nginx.png", crop_nginx)

# 4. Jenkins: x: 565..640, y: 115..190
crop_jenkins = img[115:190, 565:640]
cv2.imwrite(f"{scratch}/debug_jenkins.png", crop_jenkins)

# 5. Postgres: x: 655..745, y: 120..195
crop_pg = img[120:195, 655:745]
cv2.imwrite(f"{scratch}/debug_postgres.png", crop_pg)

# 6. MySQL: x: 725..805, y: 145..204
crop_my = img[145:204, 725:805]
cv2.imwrite(f"{scratch}/debug_mysql.png", crop_my)

# 7. RabbitMQ: x: 730..805, y: 70..145
crop_rmq = img[70:145, 730:805]
cv2.imwrite(f"{scratch}/debug_rmq.png", crop_rmq)

# 8. MDN: x: 545..605, y: 45..105
crop_mdn = img[45:105, 545:605]
cv2.imwrite(f"{scratch}/debug_mdn.png", crop_mdn)

# 9. Red streaks: x: 615..675, y: 175..204
crop_streaks = img[175:204, 615:675]
cv2.imwrite(f"{scratch}/debug_streaks.png", crop_streaks)

print("Saved all debug crops!")
