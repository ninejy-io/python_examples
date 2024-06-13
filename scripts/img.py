import random
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageFilter


im = Image.open('3e41dee77873ac6a3710d7bcdae187d2.jpeg')

print(im.format)
print(im.size)

# new_im = im.resize()
# 缩放 50%
# w, h = im.size
# im.thumbnail((w//2, h//2))
# im.save('new_50.jpeg', 'jpeg')

# 添加模糊效果
# im.filter(ImageFilter.BLUR)
# im.save('blur.jpeg', 'jpeg')

# 绘图, 生成验证码
# 随机字母
def rand_char():
    return chr(random.randint(65, 90))

# 随机颜色1
def rand_color():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2
def rand_color2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

width = 240
height = 60
im_new = Image.new('RGB', (width, height), (255, 255, 255))
font = ImageFont.truetype('consola.ttf', 36)
draw = ImageDraw.Draw(im_new)
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rand_color())
for t in range(4):
    draw.text((60 * t + 10, 10), rand_char(), font=font, fill=rand_color2())
im_new2 = im_new.filter(ImageFilter.BLUR)
im_new2.save('code.jpg', 'jpeg')
