import cv2
import numpy as np

# Let's inspect npm at y=0..15
img = cv2.imread("assets/original-footer.png")
crop_npm = img[0:52, 500:572]
cv2.imwrite("/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/tweak_npm.png", crop_npm)

# Fortran F
crop_f = img[110:192, 115:175]
cv2.imwrite("/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/tweak_f.png", crop_f)

# Chevrons
crop_chev = img[110:165, 305:352]
cv2.imwrite("/Users/nguyenvanminhtam/.gemini/antigravity-ide/brain/fc32ecfc-40ec-450f-9d01-b4d4df79dacb/scratch/tweak_chev.png", crop_chev)
print("Saved tweak crops")
