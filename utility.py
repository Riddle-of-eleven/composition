from psd_tools import PSDImage
import math

# функция, открывающая файл .psd
def open_psd_file(file_path):
    try:
        return PSDImage.open(f'images/{file_path}.psd')
    except:
        print('Не удалось открыть выбранный файл')
        return None
    
# функция, возвращающая все слои файла .psd
def get_all_layers(layer_set, layers):
    if layer_set:
        for layer in layer_set:
            if layer.is_group():
                get_all_layers(layer, layers)
            else:
                layers.append(layer)
    if layers is not None: 
        return layers
    else:
        return None

# функция поиска слоя по имени
def find_layer_by_name(file_path, name):
    psd = open_psd_file(file_path)
    if psd:
        layers = get_all_layers(psd, [])
        for layer in layers:
            if layer.name == name:
                return layer
    else:
        return None
    
# функция, возвращающая все контуры в файле .psd
# def get_all_paths(file_path):
#     psd = open_psd_file(file_path)
#     if psd:
#         print(psd.has_vector())
        # for layer in psd:
        #     if layer.has_vector_mask():
        #         print(layer.vector_mask)
        #     else:
        #         print("No Vector Mask Found")


# def get_opaque_pixels(file_path):
#     psd = open_psd_file(file_path)
#     if psd:



# математические функции

# функция расчёта угла треугольника на основе трёх сторон
def get_angle_by_sides(side_a, side_b, side_opposite):
    cos_angle = (side_a ** 2 + side_b ** 2 - side_opposite ** 2) / (2 * side_a * side_b)
    angle_radians = math.acos(cos_angle)
    return math.degrees(angle_radians)
