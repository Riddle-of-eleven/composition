import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import psd_tools
import math

import pprint

import logging
import warnings

import utility
import main_functions as main
import evaluation
import consts
from consts import Grid

# выводит сообщения только об ошибках для библиотеки psd-tools
logging.getLogger('psd_tools').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module='psd_tools')


file = 'small'

image = utility.open_psd_file(file)
# ищем слой по имени
layer = utility.find_layer_by_name('img', 'horizon')
center = utility.find_layer_by_name('img', 'center')

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
        'threshold_range': [
            int(vertical_third - grid_vertical_extension),
            int(vertical_third + grid_vertical_extension),
        ],
        # допуск точности линии
        'precision_threshold_range': [
            int(vertical_third - grid_vertical_precision_extension),
            int(vertical_third + grid_vertical_precision_extension),
        ],
        consts.main: int(vertical_third),
    },
    Grid.vr: {
        # допуск области
        'threshold_range': [
            int(vertical_third * 2 - grid_vertical_extension),
            int(vertical_third * 2 + grid_vertical_extension),
        ],
        # допуск точности линии
        'precision_threshold_range': [
            int(vertical_third * 2 - grid_vertical_precision_extension),
            int(vertical_third * 2 + grid_vertical_precision_extension),
        ],
        consts.main: int(vertical_third * 2),
    },
    Grid.ht: {
        # допуск области
        'threshold_range': [
            int(horizontal_third - grid_horizontal_extension),
            int(horizontal_third + grid_horizontal_extension),
        ],
        # допуск точности линии
        'precision_threshold_range': [
            int(horizontal_third - grid_horizontal_precision_extension),
            int(horizontal_third + grid_horizontal_precision_extension),
        ],
        consts.main: int(horizontal_third),
    },
    Grid.hb: {
        # допуск области
        'threshold_range': [
            int(horizontal_third * 2 - grid_horizontal_extension),
            int(horizontal_third * 2 + grid_horizontal_extension),
        ],
        # допуск точности линии
        'precision_threshold_range': [
            int(horizontal_third * 2 - grid_horizontal_precision_extension),
            int(horizontal_third * 2 + grid_horizontal_precision_extension),
        ],
        consts.main: int(horizontal_third * 2),
    },
}


# допуск угла
angle_threshold = 2 # в градусах

# оценка горизонта
horizon_evaluation = {
    'angle': angle_degrees,
    'position': horizon_position,
    'top_third': {
        'main': True if (horizon_position > image_thirds[Grid.ht]['threshold_range'][0]) and (horizon_position < image_thirds[Grid.ht]['threshold_range'][1]) else False,
        'precision': True if (horizon_position > image_thirds[Grid.ht]['precision_threshold_range'][0]) and (horizon_position < image_thirds[Grid.ht]['precision_threshold_range'][1]) else False,
    },
    'bottom_third': {
        'main': True if (horizon_position > image_thirds[Grid.hb]['threshold_range'][0]) and (horizon_position < image_thirds[Grid.hb]['threshold_range'][1]) else False,
        'precision': True if (horizon_position > image_thirds[Grid.hb]['precision_threshold_range'][0]) and (horizon_position < image_thirds[Grid.hb]['precision_threshold_range'][1]) else False,
    }
}


# площадь композиционного центра
# center_area = main.get_area_from_layer('img', 'center')
# пересечение с точками силы
# a1 = evaluation.check_powerpoint([image_thirds[Grid.ht][consts.main], image_thirds[Grid.vl][consts.main]], center)
# a2 = evaluation.check_powerpoint([image_thirds[Grid.ht][consts.main], image_thirds[Grid.vr][consts.main]], center)
# a3 = False
# a4 = False

# print(a1)

# оценка композиционного центра
# composition_center_evaluation = {
    # 'position': [center.top, center.left],
    # 'size': [center.width, center.height],
    # 'area_ratio': center_area / (image.width * image.height), # отношение площади композиционного центра к площади изображения
    # 'area': center_area,
    # 'powerpoint': {
    #     'a1': True if ()
    # }
# }

# pprint.pprint(composition_center_evaluation)



# получение слоя в виде numpy массива
# center_layer = utility.find_layer_by_name(file, 'center')
# composite = center_layer.composite()
# array = utility.convert_to_gray(np.array(composite))



# нахождение объекта в пределах линии сетки

# background = utility.find_layer_by_name(file, 'image')
# gray_image = utility.convert_to_gray(background.composite())

# left = center_layer.left
# top = center_layer.top

# правая вертикальная
# flag = 0
# for i in range(center_layer.width):
#     position = i + left
#     # print(f"{image_thirds[Grid.vr]['threshold_range'][0]}, {image_thirds[Grid.vr]['threshold_range'][1]}")
#     if (array[0][i] != 255) and (position > image_thirds[Grid.vr]['threshold_range'][0]) and (position < image_thirds[Grid.vr]['threshold_range'][1]):
#         print(f"элемент: {array[0][i]}, позиция: {position}")
#         flag += 1

# percentage = flag / center_layer.width
# print(percentage)

from_psd = utility.psd_to_numpy(file, 'background')
m = utility.show_image_with_grid(from_psd, image_thirds)
print(from_psd)
# utility.show_image(m, True)
# utility.show_image(from_psd, True)