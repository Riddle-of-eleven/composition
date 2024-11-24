import numpy as np
import cv2
import matplotlib.pyplot as plt
import psd_tools

import utility

import logging
import warnings

logging.getLogger('psd_tools').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module='psd_tools')


image = utility.find_layer_by_name('red', 'blue')
composite = image.composite()
array = utility.convert_to_gray(np.array(composite))


print(array)

utility.show_image(array, True)
