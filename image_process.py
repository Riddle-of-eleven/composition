## БИБЛИОТЕКИ И ИМПОРТ ФАЙЛОВ

# основное
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import psd_tools
import math

# ошибки и логирование
import logging
import warnings

# собственное
import utility
import main_functions as main
import evaluation
from consts import Grid
import lib.analyse.thirds as thirds
import lib.helpers as helpers
import lib.helpers.psd as psd
import lib.helpers.emphasis as emphasis

###########


## СЛУЖЕБНОЕ

# выводит сообщения только об ошибках для библиотеки psd-tools
logging.getLogger('psd_tools').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module='psd_tools')


###########


file = 'cat'

# image – открытый файл .psd
image = utility.open_psd_file(file)

# width, height – высота и ширина исходного изображения
width, height = image.size


# print(psd.get_area_ratio(image, 'background'))
# print(thirds.check_impresses(image, 'center'))

# thirds.show_image_with_grid(image)

# print(thirds.init_grid(image))

# print(saliency.normalize_map(image))
# emphasis.get_weights_map(image, emphasis.normalize_map(image))


# print(psd.psd_to_grayscale(image, 'body'))
# print(psd.get_image(image, 'body'))
# print(psd.visualize(image, 'body'))


# thirds.evaluate_composition_center(image, 3)




### СЕТКА
# инициализация сетки изображения (дефолтной)
grid = thirds.init_grid(image)

# визуализация изображения с учётом сетки
# thirds.show_image_with_grid(image)


### ОБЪЕКТ (ЦЕНТР)
# положение центра
center_position = psd.get_layer_coordinates(image, 'center')
# проверка расположения в паверпоинтах
center_impress = thirds.check_impresses(image, 'center')
# print(thirds.interpret(points=center_impress))
# проверка расположения по линиям
center_line = thirds.check_lines(image, 'center')
# for index, line in center_line.items():
#     print(index, thirds.interpret(range=line))
# проверка расположения по прямоугольникам
center_rectangle = thirds.check_rectangles(image, 'center')
# for rect in center_rectangle:
#     print(thirds.interpret(rectangle=rect))

# площадь пересечения объекта и области линии (численно и в процентах от общей площадии объекта)
center_range_intersect = thirds.range_intersections(image, 'center')
# интерпретация данных пересечения
interpret = thirds.evaluate_composition_center(image, 3)
# print(interpret)


### ГОРИЗОНТ
# положение горизонта
# horizon_position = psd.get_layer_coordinates(image, 'horizon')
# угол наклона
# horizon_angle = thirds.horizon_angle(image)
# проверка расположения по линиям сетки
# horizon_ev = thirds.check_horizon(image)



### ПРОЧИЕ ДАННЫЕ ПО СЛОЯМ
# соотношение площади неба и изображения
# sky_area_ratio = psd.get_area_ratio(image, 'sky')
# то же самое про землю
# ground_area_ratio = psd.get_area_ratio(image, 'ground')
# и про центр композиционный
# center_area_ratio = psd.get_area_ratio(image, 'center')

# print(center_area_ratio)