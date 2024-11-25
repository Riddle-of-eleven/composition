from psd_tools import PSDImage
import numpy as np

# функция, открывающая файл .psd
def open_psd_file(file_path):
    try:
        return PSDImage.open(f'images/{file_path}.psd')
    except:
        print('Не удалось открыть выбранный файл')
        return None


# .psd-файл передаётся на вход функциям (кроме первой), поэтому его предварительно надо открыть

# функция получения всех слоёв
def get_layers(psd, out=[]):
    if psd:
        for layer in psd:
            if layer.is_group(): 
                get_layers(layer, out)
            else:
                out.append(layer)
    if out is not None: return out
    else: return None

# функция поиска слоя по имени
def get_layer(psd, layer_name):
    for layer in psd:
        if layer.name == layer_name:
            return layer
    return None


##############

## ФУНКЦИИ, СВЯЗАННЫЕ С КОМПОЗИЦИЕЙ

# функция, получающая площадь слоя
def get_layer_area(psd, layer_name):
    layer = get_layer(psd, layer_name)
    if layer:
        image = layer.topil()
        # возвращает количество непрозрачных пикселей (полупрозрачные тоже входят в площадь)
        area = sum(1 for pixel in image.getdata() if pixel[3] != 0) if image.mode == 'RGBA' else image.width * image.height
        return area
    else:
        return None

# функцция, вычисляющая соотношение площади объекта и изображения в целом
def get_area_ratio(psd, layer_name):
    area = get_layer_area(psd, layer_name)
    if area and psd:
        image_area = psd.width * psd.height
        return area / image_area
    else: 
        return None
    
# функция определения координатов объекта
def get_layer_coordinates(psd, layer_name):
    layer = get_layer(psd, layer_name)
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




# конвертация .psd в массив numpy
def psd_to_numpy(psd):
    return np.array(psd.composite())