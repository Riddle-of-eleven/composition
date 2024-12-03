from psd_tools import PSDImage
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

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
        if layer.is_group():
            layer = get_layer(layer, layer_name)
        if (layer is not None) and (layer.name == layer_name):
                return layer
    return None

# функция, возвращающая композицию слоёв или слой по имени в виде numpy 
        # потому что composite() возвращает PIL
def get_image(psd, layer_name=None):
    if layer_name: 
        layer = get_layer(psd, layer_name)
        if layer is None: raise Exception('Выбранного слоя не существует')
        
        return np.array(layer.composite(psd.bbox, color=(0,0,0)))
    return np.array(psd.composite())



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


# функция, вычисляющая угол наклона линии по сторонам треугольника (половинки прямоугольника) из слоя
def get_line_angle(psd, layer_name):
    layer = get_layer(psd, layer_name)
    # стороны
    width = layer.width
    height = layer.height
    if height == 1: # в случае абсолютно ровной линии (иначе будет считать доли градуса из-за 1 пикселя)
        return 0
    else:
        hypotenuse = math.sqrt(width ** 2 + height ** 2)
        print(width, height, hypotenuse)
        # косинус угла
        cos_angle = (width ** 2 + hypotenuse ** 2 - height ** 2) / (2 * width * hypotenuse)
        # угол в градусах
        angle_radians = math.acos(cos_angle)
        return math.degrees(angle_radians)


##############

## СВЯЗАННОЕ С АНАЛИЗОМ ИЗОБРАЖЕНИЯ

# функция, получающая на изображении или выбранном слое оттенки серого
def get_shades(psd, layer=None):
    if type(psd) is not np.ndarray:
        psd = get_image(psd, layer)

    colors = set()
    for index, row in enumerate(psd):
        for pixel in row:
            colors.add(int(pixel))
    return sorted(colors, reverse=True)


##############

## ВСЯКИЕ СЛУЖЕБНЫЕ ФУНКЦИИ

# функция, преобразующая .psd массив numpy в оттенках серого
def psd_to_grayscale(psd, layer=None):
    psd = get_image(psd, layer)
    return cv2.cvtColor(psd, cv2.COLOR_RGB2GRAY)



##############

## ВИЗУАЛИЗАЦИЯ

# функция, визуализирующая изображение
def visualize(psd, layer=None, gray=None):
    psd = get_image(psd, layer)

    fig, _ = plt.subplots() # подчёркивание для корректной деструктуризации кортежа
    fig.patch.set_facecolor('lightblue') # фон окна

    if gray is None: plt.imshow(psd)
    else: plt.imshow(psd, cmap='gray')
    
    plt.axis('off')
    plt.show()