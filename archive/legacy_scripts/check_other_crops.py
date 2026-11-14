from PIL import Image

img = Image.open('paper/figures/figure1_monthly_nss_trajectory.png')
w, h = img.size

# COVID-19 (x ~ 0.35 * w, y ~ bottom 0.65 to 0.95 * h)
crop_covid = img.crop((int(0.28 * w), int(0.65 * h), int(0.48 * w), int(0.95 * h)))
crop_covid.save('paper/figures/crop_covid_check.png')

# BL Hotfix (x ~ 0.70 * w, y ~ bottom 0.65 to 0.95 * h)
crop_bl = img.crop((int(0.68 * w), int(0.65 * h), int(0.88 * w), int(0.95 * h)))
crop_bl.save('paper/figures/crop_bl_check.png')

# 5G Launch (x ~ 0.82 * w, y ~ top 0.05 to 0.35 * h)
crop_5g = img.crop((int(0.80 * w), int(0.04 * h), int(0.98 * w), int(0.35 * h)))
crop_5g.save('paper/figures/crop_5g_check.png')
