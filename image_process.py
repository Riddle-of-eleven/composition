import cv2
import numpy
import matplotlib
import psd_tools
import math

import pprint

import logging
import warnings

import utility
import consts
from consts import Grid

# выводит сообщения только об ошибках для библиотеки psd-tools
logging.getLogger('psd_tools').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module='psd_tools')



image = utility.open_psd_file('img')
# ищем слой по имени
layer = utility.find_layer_by_name('img', 'horizon')

# стороны
width = layer.width
height = layer.height
hypotenuse = math.sqrt(width ** 2 + height ** 2)
# угол
angle_degrees = utility.get_angle_by_sides(width, hypotenuse, height)
# положение горизонта
horizon_position = layer.top


# стороны изображения
width = image.width
height = image.height


# TODO: добавить разные допуски на разные линии (в зависимости от того, в каком месте больше внимания и какая линия допускает больший разброс)

# допуски сетки (измеряются в процентах)
threshold = 0.05
precision_threshold = 0.01

# расширение сетки по основному допуску
grid_horizontal_extension = height * threshold
grid_vertical_extension = width * threshold
# расширение сетки по допуску точности
grid_horizontal_precision_extension = height * precision_threshold
grid_vertical_precision_extension = width * precision_threshold

# сетка
vertical_third = width / 3
horizontal_third = height / 3
image_thirds = {
    Grid.vl: {
        # допуск области
        'threshold_range': {
            consts.left: int(vertical_third - grid_vertical_extension),
            consts.right: int(vertical_third + grid_vertical_extension),
        },
        # допуск точности линии
        'precision_threshold_range': {

        },

        consts.main: int(vertical_third),
    },
    Grid.vr: {
        consts.left: int(vertical_third * 2 - grid_vertical_extension),
        consts.right: int(vertical_third * 2 + grid_vertical_extension),
        consts.main: int(vertical_third * 2),
    },
    Grid.ht: {
        consts.top: int(horizontal_third - grid_horizontal_extension),
        consts.bottom: int(horizontal_third + grid_horizontal_extension),
        consts.main: int(horizontal_third),
    },
    Grid.hb: {
        consts.top: int(horizontal_third * 2 - grid_horizontal_extension),
        consts.bottom: int(horizontal_third * 2 + grid_horizontal_extension),
        consts.main: int(horizontal_third * 2),
    },
}


# horizontal_range = {
#     'top': image_thirds[Grid.ht] - grid_horizontal_extension,
#     'bottom': image_thirds[Grid.ht] + grid_horizontal_extension,
# }

# разница между значениями horizon и третей
# horizon_diff = True if (horizon_position > horizontal_range[Grid.top]) and (horizon_position < horizontal_range[Grid.bottom]) else False

# print(f'горизонт {horizon_position}')
# print(f'диапазон сверху {horizontal_range[Grid.top]}')
# print(f'диапазон снизу {horizontal_range[Grid.bottom]}')
# print(f'верхняя линия {image_thirds[Grid.ht]}')
# print(horizon_diff)

print(f'верхняя горизонтальная {image_thirds[Grid.ht]}')