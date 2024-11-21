import utility

def check_powerpoint(point, object):
    '''
    Определение расположения объекта в пределах точки
    '''
    if object.top <= point[0] <= object.bottom and object.left <= point[1] <= object.right:
        return True
    else:
        return False