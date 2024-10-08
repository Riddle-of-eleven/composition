from PIL import Image

image = Image.open('images/ten.png')

if image.mode == 'RGBA':
    pixels = image.getdata()
    nontransparent_pixels = sum(1 for pixel in pixels if pixel[3] == 255)

    print(nontransparent_pixels)
else:
    print('aaaa')