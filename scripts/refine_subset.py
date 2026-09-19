import cv2
import numpy as np

img = cv2.imread("assets/original-footer.png")
scratch = "/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch"

# Kafka: 690 to 805, 85 to 150
crop_kafka = img[85:150, 690:805]
cv2.imwrite(f"{scratch}/refine_kafka.png", crop_kafka)

# Kubernetes: 805 to 875, 80 to 148
crop_k8s = img[80:148, 805:875]
cv2.imwrite(f"{scratch}/refine_k8s.png", crop_k8s)

# Mini Gophers: 795 to 870, 134 to 180
crop_pair = img[134:180, 795:870]
cv2.imwrite(f"{scratch}/refine_pair.png", crop_pair)

# GoLand: 480 to 548, 50 to 120
crop_goland = img[50:120, 480:548]
cv2.imwrite(f"{scratch}/refine_goland.png", crop_goland)

# Jenkins: 565 to 645, 115 to 190
crop_jenkins = img[115:190, 565:645]
cv2.imwrite(f"{scratch}/refine_jenkins.png", crop_jenkins)

# Nginx: 580 to 670, 40 to 158
crop_nginx = img[40:158, 580:670]
cv2.imwrite(f"{scratch}/refine_nginx.png", crop_nginx)

print("Saved refine crops!")
