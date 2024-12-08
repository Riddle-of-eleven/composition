import lib.analyse.thirds as thirds
import lib.helpers.psd as psd
import lib.analyse.guide as guide

import logging
import warnings

# выводит сообщения только об ошибках для библиотеки psd-tools
logging.getLogger('psd_tools').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module='psd_tools')

file = 'line'
image = psd.open_psd_file(file)

# grid = thirds.init_grid(image)['grid']
# print(thirds.range_intersections(image, 'center'))

#print(guide.line_object_intersection(image, 'line', 'object'))

print(psd.get_image(image, 'transparent'))