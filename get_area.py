from PIL import Image

def get_nontransparent_area(image_name, image_format):
    image = Image.open(f'images/{image_name}.{image_format}')
    if image.mode == 'RGBA':
        # getdata возвращает содержимое изображения в виде набора объектов
        nontransparent_pixels = sum(1 for pixel in image.getdata() if pixel[3] != 0)
        return nontransparent_pixels
    else:
        return image.width * image.height


area = get_nontransparent_area('ten', 'png')