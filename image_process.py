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

###########


## СЛУЖЕБНОЕ

# выводит сообщения только об ошибках для библиотеки psd-tools
logging.getLogger('psd_tools').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module='psd_tools')


###########


file = 'small'

# image – открытый файл .psd
image = utility.open_psd_file(file)

# width, height – высота и ширина исходного изображения
width, height = image.size


# print(psd.get_area_ratio(image, 'background'))
# print(thirds.check_impress_all(image, 'center'))

thirds.show_image_with_grid(image)
