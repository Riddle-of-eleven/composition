from psd_tools import PSDImage

# Функция определения площади объекта из файла .psd
def get_area_from_psd(file_path):
    psd = PSDImage.open(f'images/{file_path}.psd')

    layer_object_name = 'object'
    layer_background_name = 'image'

    object = None
    background = None

    for layer in psd:
        if not(layer.is_group()):
            if layer.name == layer_object_name:
                object = layer
            elif layer.name == layer_background_name:
                background = layer

    if object is not None:
        image = object.topil()
        # getdata возвращает содержимое изображения в виде набора объектов
        area = sum(1 for pixel in image.getdata() if pixel[3] != 0) if image.mode == 'RGBA' else image.width * image.height

        return area
    else:
        return None

print(get_area_from_psd('2'))