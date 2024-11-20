from psd_tools import PSDImage
import utility

CURRENT_FILE = 'gl_1'

# Функция определения площади объекта из файла .psd
def get_area_from_psd(file_path):
    psd = utility.open_psd_file(file_path)

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

# функция, вычисляющая площадь объекта на заданном слое (количество пикселей)
def get_area_from_layer(file_path, layer_name):
    layer = utility.find_layer_by_name(file_path, layer_name)
    if layer:
        image = layer.topil()
        # возвращает количество непрозрачных пикселей (полупрозрачные тоже входят в площадь)
        area = sum(1 for pixel in image.getdata() if pixel[3] != 0) if image.mode == 'RGBA' else image.width * image.height
        return area
    else:
        return None

# функция, определяющая координаты объекта
def get_layer_coordinates(file_path, layer_name):
    layer = utility.find_layer_by_name(file_path, layer_name)
    if layer:
        # слева – сверху – справа – снизу
        # return layer.bbox
        return {
            'top_left': {'x': layer.left, 'y': layer.top},
            'top_right': {'x': layer.left + layer.width, 'y': layer.top},
            'bottom_right': {'x': layer.left + layer.width, 'y': layer.top + layer.height},
            'bottom_left': {'x': layer.left, 'y': layer.top + layer.height},
        }

    else:
        print('Не удалось получить координаты объекта')
        return None
    
# функцция, вычисляющая соотношение площади объекта и изображения в целом
def get_area_ratio(file_path, layer_name):
    area = get_area_from_layer(file_path, layer_name)
    image = utility.open_psd_file(file_path)
    if area and image:
        image_area = image.width * image.height
        return area / image_area
    else: 
        return None

# функция, получающая угол наклона горизонта (линия горизонта содержится в контуре)
# def get_horison_angle(file_path, layer_name):


print(utility.get_all_paths(CURRENT_FILE))