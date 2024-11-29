from ..helpers import psd as psd_helper
from matplotlib import pyplot as plt


# функция инициализации сетки (по открытому файлу .psd)
# ПОТОМ: добавить разные допуски на разные линии (в зависимости от того, в каком месте больше внимания и какая линия допускает больший разброс)
def init_grid(image):
    # размеры исходного изображения
    width, height = image.size

    # допуски сетки (измеряются в процентах)
    threshold = 0.05
    precision_threshold = 0.01

    # расширение сетки по основному допуску
    vertical_ext = width * threshold
    horizontal_ext = height * threshold
    # расширение сетки по допуску точности
    vertical_precision_ext = width * precision_threshold
    horizontal_precision_ext = height * precision_threshold
    # расширение сетки по допуску отображения
    display_ext = 3

    # размер шага сетки
    vertical = width / 3
    horizontal = height / 3

    return {
        'grid': {
            'vl': {
                #собственно, линия
                'line': round(vertical),
                # допуск области
                'range': [round(vertical - vertical_ext), round(vertical + vertical_ext)],
                # допуск точности линии
                'precision': [round(vertical - vertical_precision_ext), round(vertical + vertical_precision_ext)],
                'display': [round(vertical - display_ext), round(vertical + display_ext)],
            },
            'vr': {
                'line': round(vertical * 2),
                'range': [round(vertical * 2 - vertical_ext), round(vertical * 2 + vertical_ext)],
                'precision': [round(vertical * 2 - vertical_precision_ext), round(vertical * 2 + vertical_precision_ext)],
                'display': [round(vertical * 2 - display_ext), round(vertical * 2 + display_ext)],
            },
            'ht': {
                'line': round(horizontal),
                'range': [round(horizontal - horizontal_ext), round(horizontal + horizontal_ext)],
                'precision': [round(horizontal - horizontal_precision_ext), round(horizontal + horizontal_precision_ext)],
                'display': [round(horizontal - display_ext), round(horizontal + display_ext)],
            },
            'hb': {
                'line': round(horizontal * 2),
                'range': [round(horizontal * 2 - horizontal_ext), round(horizontal * 2 + horizontal_ext)],
                'precision': [round(horizontal * 2 - horizontal_precision_ext), round(horizontal * 2 + horizontal_precision_ext)],
                'display': [round(horizontal * 2 - display_ext), round(horizontal * 2 + display_ext)],
            },
        },
        'impress': [
            # ПО ЧАСОВОЙ СТРЕЛКЕ
            [round(vertical), round(horizontal)],
            [round(vertical * 2), round(horizontal)],
            [round(vertical * 2), round(horizontal * 2)],
            [round(vertical), round(horizontal * 2)],
        ]
        
    }

# функция проверки нахождения объекта (на заданном слое) в конкретной точке силы
# это каррирование, к слову, надо, чтобы функцию удобно применить
def check_impress(psd, layer_name):
    def point(point):
        layer = psd_helper.get_layer(psd, layer_name)
        if (layer.left <= point[0]) and (layer.left + layer.width >= point[0]) and (layer.top <= point[1]) and (layer.top + layer.height >= point[1]):
            return True
        return False
    return point

# функция проверки нахождения в каждой точке силы
def check_impress_all(psd, layer_name):
    grid = init_grid(psd)['impress']
    check = check_impress(psd, layer_name)
    return [
        check(grid[0]), check(grid[1]), check(grid[2]), check(grid[3]),
    ]

# функция оценки композиционного центра (.psd)
# def evaluate_composition_center(image):
#     center = 



###########

## ВИЗУАЛИЗАЦИЯ

# функция вывода изображения с сеткой
def show_image_with_grid(psd):
    grid = init_grid(psd)
    image = psd_helper.psd_to_numpy(psd)

    canvas = [[255 for col in range(psd.width)] for row in range(psd.height)]

    for index, row in enumerate(canvas):
        # замена элементов ряда в соответствии с индексами столбцов

        # левая треть
        grid_vl = grid['grid']['vl']['display']
        vl = grid_vl[0]
        while vl <= grid_vl[1]:
            row[vl] = 0
            vl += 1
        # правая треть
        grid_vr = grid['grid']['vr']['display']
        vr = grid_vr[0]
        while vr <= grid_vr[1]:
            row[vr] = 0
            vr += 1
        
        grid_ht = grid['grid']['ht']['display']
        grid_hb = grid['grid']['hb']['display']

        if (grid_ht[0] - 1 <= index <= grid_ht[1] - 1) or (grid_hb[0] - 1 <= index <= grid_hb[1] - 1):
            # замена ряда целиком на 0
            canvas[index] = list(map(lambda x: 0, row))
    
    # print(canvas)
    
    plt.imshow(image)
    plt.imshow(canvas, cmap='gray', alpha=0.2)
    plt.axis('off')
    plt.show()


