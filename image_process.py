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


file = 'test/bp'

# image – открытый файл .psd
image = utility.open_psd_file(file)

# width, height – высота и ширина исходного изображения
width, height = image.size


# print(psd.get_area_ratio(image, 'background'))
# print(thirds.check_impress_all(image, 'center'))

# thirds.show_image_with_grid(image)

# print(thirds.init_grid(image))

# print(saliency.normalize_map(image))
# emphasis.get_weights_map(image, emphasis.normalize_map(image))


# print(psd.psd_to_grayscale(image, 'body'))
# print(psd.get_image(image, 'body'))
print(psd.visualize(image, 'body'))