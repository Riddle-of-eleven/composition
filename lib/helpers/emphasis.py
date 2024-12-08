import numpy as np
from ..helpers import psd as psd
import matplotlib.pyplot as plt

# имитация saliency map

layer_name = 'emphasis'

# определение значимости пипеткой с карты

# функция, получающая и нормализующая значения карты 255..0 в 0..1
def normalize_map(image):
    image = psd.psd_to_grayscale(image, layer_name)
    shades = np.array(psd.get_shades(image))
    invert = 255 - shades # инвертирование исходных значений, чтобы 0 не был самым маленьким значением

    # нормализация через сигмоиду, но всё делится на delimiter, чтобы не приближаться к потолку самой сигмоиды
    k = 2  # растяжение графика, отвечает за большую плавность роста значений
    shift = 1  # сдвиг куда-то там, это экспериментально подбиралось
    delimiter = 100  # деление вот на это увеличивает разницу между близкими элементами
    
    norm = 1 / (1 + np.exp(-k * (invert / delimiter - shift)))

    return dict(zip(shades, norm)) # запихивает массивы как [ключ:значение] в один словарь


# функция, определяющая карту весов исходя из карты значений 
def get_weights_map(image, emph_map, layer=None): 
    image = psd.psd_to_grayscale(image, layer) 
    
    map = []
    for row in image:  # ОПТИМИЗИРОВАТЬ!!!!!!
        for pixel in row:
            map.append(float(emph_map[pixel]))
    return map