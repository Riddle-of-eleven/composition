from ..helpers import psd

# функция, проверяющая пересечение линии и объекта
def line_object_intersection(image, line_layer, object_layer):
    line = psd.get_layer(image, line_layer)
    object = psd.get_layer(image, object_layer)

    intersect = []

    # наклон вправо
    A1 = [line.left + 1, line.top + line.height]
    B1 = [line.left + line.width, line.top + 1]

    k1 = (B1[1] - A1[1]) / (B1[0] - A1[0])
    b1 = A1[1] - k1 * A1[0]
    # y = kx + b => b = y - kx

    res1 = False
    for i in range(object.left + 1, object.left + object.width + 1): # +1 затем, чтобы считалась именно область объекта
        if (object.top <= k1 * i + b1 <= object.top + object.height):
            res1 = True
            break
    intersect.append(res1)

    # наклон влево
    A2 = [line.left, line.top]
    B2 = [line.left + line.width, line.top + line.height]

    k2 = (B2[1] - A2[1]) / (B2[0] - A2[0])
    b2 = A2[1] - k2 * A2[0]
 
    res2 = False
    for i in range(object.left + 1, object.left + object.width + 1):
        if (object.top <= k2 * i + b2 <= object.top + object.height):
            res2 = True
            break
    intersect.append(res2)


    return intersect