from PIL import Image
from pathlib import Path

img = Image.open('paper/figures/figure1_monthly_nss_trajectory.png')
w, h = img.size
print(f"Image dimensions: {w} x {h}")

# Crop the 4G region:
# In an image of w=4050, h=1920:
# 4G is around x = 19/123 * w ~ 625. y is around top (y = 80 in [-75, 112] scale ~ (112 - 80)/(112 - -75) * h ~ 328)
box_4g = (int(0.12 * w), int(0.08 * h), int(0.28 * w), int(0.35 * h))
crop_4g = img.crop(box_4g)
crop_4g.save('paper/figures/crop_4g_check.png')

print("Cropped 4G region saved to paper/figures/crop_4g_check.png")
