import cv2
import numpy as np

img = cv2.imread("/Users/nguyenvanminhtam/nvmtamm/assets/original-footer.png")
h, w = img.shape[:2]

# The central area where icons reside is x roughly 100 to 920, y 0 to 204
# The left (0 to 100) and right (920 to 1024) have glowing orange circuit traces
# Let's inspect the background color
# In dark areas between icons, pixels have low intensity in R, G, B
# e.g., B < 65, G < 40, R < 40

# Let's define known icons with their approximate centers / bounding boxes
# so we extract them with maximum fidelity and name them properly!
# Let's inspect the list of icons:
# 1. Gulp: (x: 120-175, y: 15-85)
# 2. Cinema 4D / '4': (x: 170-245, y: 10-105)
# 3. Debian: (x: 245-310, y: 5-85)
# 4. gRPC: (x: 320-440, y: 10-80)
# 5. Photoshop 'Ps': (x: 440-490, y: 25-85)
# 6. npm: (x: 505-565, y: 15-70)
# 7. GO speed: (x: 565-645, y: 15-80)
# 8. Discord/Robot bot: (x: 645-690, y: 30-80)
# 9. React: (x: 690-750, y: 25-95)
# 10. Elastic: (x: 750-805, y: 30-95)
# 11. Illustrator 'Ai': (x: 805-855, y: 30-85)
# 12. Swift: (x: 95-160, y: 100-165)
# 13. '<e>': (x: 165-225, y: 110-165)
# 14. GitHub Octocat: (x: 225-285, y: 110-180)
# 15. Docker whale: (x: 280-380, y: 70-155)
# 16. Git: (x: 375-430, y: 95-155)
# 17. Redis: (x: 420-475, y: 115-180)
# 18. GoLand/Go square: (x: 475-535, y: 95-160)
# 19. Nginx: (x: 585-640, y: 115-185)
# 20. Sketch: (x: 635-695, y: 95-155)
# 21. Jenkins: (x: 575-625, y: 160-204)
# 22. PostgreSQL: (x: 660-735, y: 135-204)
# 23. Kafka: (x: 690-785, y: 105-160)
# 24. MySQL: (x: 730-805, y: 160-204)
# 25. Kubernetes: (x: 805-865, y: 100-165)
# 26. Pink & Purple Gophers: (x: 820-880, y: 155-204)
# 27. AppStore/Xcode: (x: 850-930, y: 115-204)
# 28. Big Go Gopher: (x: 440-540, y: 145-204)
# 29. JS: (x: 385-435, y: 165-204)
# 30. GitLab: (x: 345-395, y: 175-204)
# 31. Apple: (x: 250-310, y: 170-204)
# 32. 3D Cube/Hexagon (blue): (x: 165-230, y: 160-204)
# 33. F# / 3D block: (x: 120-175, y: 150-204)
# 34. Wireshark fin / blue fin: (x: 315-365, y: 180-204)
# 35. HTML5 / Webpack badge: (x: 410-450, y: 190-204)
# 36. Spring / circular dots: (x: 105-155, y: 180-204)
# 37. Eagle / Blue bird: (x: 855-915, y: 25-95)

print("Icons categorized!")
