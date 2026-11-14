from PIL import Image

img = Image.open('paper/figures/figure1_monthly_nss_trajectory.png')
w, h = img.size

# Wider box to see full 4G text
box_4g = (int(0.12 * w), int(0.08 * h), int(0.35 * w), int(0.35 * h))
crop_4g = img.crop(box_4g)
crop_4g.save('paper/figures/crop_4g_check_wide.png')
