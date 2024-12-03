from ..helpers import psd
from matplotlib import pyplot as plt


# функция инициализации сетки (по открытому файлу .psd)
# ПОТОМ: добавить разные допуски на разные линии (в зависимости от того, в каком месте больше внимания и какая линия допускает больший разброс)
def init_grid(image):
    # размеры исходного изображения
    width, height = image.size

    # допуски сетки (измеряются в процентах)
    threshold = 0.05
    precision_threshold = 0.01
    im_threshold = 0.1

    # расширение сетки по основному допуску
    vertical_ext = width * threshold
    horizontal_ext = height * threshold
    # расширение сетки по допуску точности
    vertical_precision_ext = width * precision_threshold
    horizontal_precision_ext = height * precision_threshold
    # расширение сетки по допуску отображения
    display_ext = 3

    # расширение импресса до прямоугольника
    im_vertical_ext = width * im_threshold
    im_horizontal_ext = height * im_threshold

    # размер шага сетки
    vertical = width / 3
    horizontal = height / 3

    # способ задания сетки громоздкий, потом улучшить!!!!!
    return {
        'grid': {
            'vl': {
                #собственно, линия
                'line': round(vertical),
                # допуск области
                'range': [round(vertical - vertical_ext), round(vertical + vertical_ext)],
                # допуск точности линии
                'precision': [round(vertical - vertical_precision_ext), round(vertical + vertical_precision_ext)],
                # допуск отображения линии
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
        'rectangle': [
            { # левый верхний
                'y1': (round(vertical - im_vertical_ext)),
                'y2': (round(vertical + im_vertical_ext)),
                'x1': (round(horizontal - im_horizontal_ext)),
                'x2': (round(horizontal + im_horizontal_ext)),
            },
            { # правый верхний
                'y1': (round(vertical * 2 - im_vertical_ext)),
                'y2': (round(vertical * 2 + im_vertical_ext)),
                'x1': (round(horizontal - im_horizontal_ext)),
                'x2': (round(horizontal + im_horizontal_ext)),
            },
            { # правый нижний
                'y1': (round(vertical * 2 - im_vertical_ext)),
                'y2': (round(vertical * 2 + im_vertical_ext)),
                'x1': (round(horizontal * 2 - im_horizontal_ext)),
                'x2': (round(horizontal * 2 + im_horizontal_ext)),
            },
            { # левый нижний
                'y1': (round(vertical - im_vertical_ext)),
                'y2': (round(vertical + im_vertical_ext)),
                'x1': (round(horizontal * 2 - im_horizontal_ext)),
                'x2': (round(horizontal * 2 + im_horizontal_ext)),
            },
        ],
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
def check_impress(image, layer_name):
    def point(point):
        layer = psd.get_layer(image, layer_name)
        if (layer.left <= point[0]) and (layer.left + layer.width >= point[0]) and (layer.top <= point[1]) and (layer.top + layer.height >= point[1]):
            return True
        return False
    return point
# функция проверки нахождения в каждой точке силы
def check_impresses(image, layer_name):
    grid = init_grid(image)['impress']
    check = check_impress(image, layer_name)
    return [
        # верхняя левая, верхняя правая, нижняя правая, нижняя левая
        check(grid[0]), check(grid[1]), check(grid[2]), check(grid[3]),
    ]

# функция проверки нахождения в областях линий сетки
def check_line(image, layer_name, grid):
    def line(line_name):
        layer = psd.get_layer(image, layer_name)
        line = grid[line_name]
        diff = []
        # передаём именно линию (то есть vl, vr, ht, hb)
        if (line_name == 'vl') or (line_name == 'vr'):
            diff.append([
                layer.left - line['range'][0], #ll
                (layer.left + layer.width) - line['range'][0], # rl
            ])
            diff.append([
                layer.left - line['range'][1], # lr
                (layer.left + layer.width) - line['range'][1], # rr
            ])
        else:
            diff.append([
                layer.top - line['range'][0], #ll
                (layer.top + layer.height) - line['range'][0], # rl
            ])
            diff.append([
                layer.top - line['range'][1], # lr
                (layer.top + layer.height) - line['range'][1], # rr
            ])
        return diff
    return line
# функция проверки нахождения во всех линиях
def check_lines(image, layer_name):
    grid = init_grid(image)['grid']
    check = check_line(image, layer_name, grid)
    return {
        'vl': check('vl'),
        'vr': check('vr'),
        'ht': check('ht'),
        'hb': check('hb'),
    }

# функция проверки нахождения объекта в прямоугольнике
def check_rectangle(image, layer_name, rect):
    return 'абоба'
# функция проверки нахождения во всех прямоугольниках
def check_rectangles(image, layer_name):
    return 'абоба'


# функция, дающая интерпретацию положения объекта на основе данных о положении относительно линии
def interpret(points=None, range=None):
    if points:
        a1, a2, a3, a4 = points
        if (not a1 and not a2 and not a3 and not a4): return 'Объект не находится ни в одной точке'
        else:
            str = 'Объект находится в точках: '
            if a1: str += '\n-верхняя левая'
            if a2: str += '\n-верхняя правая'
            if a3: str += '\n-нижняя правая'
            if a4: str += '\n-нижняя левая'
            return str
    if range:
        if (range[0][0] > 0) and (range[1][1] < 0): return 'Объект внутри области'
        elif (range[0][0] < 0) and (range[1][1] > 0): return 'Объект выходит за пределы области с обеих сторон'
        elif ((range[0][0] < 0) and (range[0][1] < 0)) or ((range[1][0] > 0) and (range[1][1] > 0)): return 'Объект не пересекает область'
        elif (range[0][0] > 0) and (range[0][1] > 0): return 'Объект пересекает область справа/снизу'
        elif (range[1][0] < 0) and (range[1][1] < 0): return 'Объект пересекает область слева/сверху'



# функция оценки композиционного центра (.psd)
def evaluate_composition_center(image, n=1):
    # в общем случае вес множества определяется числом, которое около него стоит (то есть индекс=вес)
    # при переводе этого дела в формат (файловый или ещё какой) поменять

    grid = init_grid(image)
    centers = dict()
    for i in range(1, n + 1):
        center = psd.get_layer(image, f"center{i}")
        if center: centers.update({i: center})

    evaluate_centers = dict()
    # нуждается в оптимизации
    for index, center in centers.items():
        # паверпоинты импрессы
        points = check_impresses(image, f'center{index}')
        # линии
        lines = check_lines(image, f'center{index}')
        # прямоугольники
        rectangles = check_rectangles(image, f'center{index}')


###########

## ВИЗУАЛИЗАЦИЯ

# функция вывода изображения с сеткой
def show_image_with_grid(image):
    grid = init_grid(image)
    # print(image.width, image.height)
    # print(grid)
    working_image = psd.get_image(image)

    # здесь происходит заполнение пустого массива (изображения) белыми пикселями
    canvas = [[255 for col in range(image.width)] for row in range(image.height)]

    print(image.width)

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
    
    plt.imshow(working_image)
    plt.imshow(canvas, cmap='gray', alpha=0.2)
    plt.axis('off')
    plt.show()


