import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_fourie(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    ft = np.fft.fft2(image) # дискретное преобразование Фурье
    ft_shifted = np.fft.fftshift(ft) # сдвиг центра

    height, width = image.shape
    radius = 30  # радиус круга сохранения низких частот
    high_pass_filter_mask = np.ones((height, width), np.uint8)
    cv2.circle(high_pass_filter_mask, (width // 2, height // 2), radius, 0, -1)

    ft_filtered = ft_shifted * high_pass_filter_mask

    filtered_image = np.fft.ifft2(np.fft.ifftshift(ft_filtered)).real # обратное преобразование
    magnitude_spectrum = np.log(np.abs(ft_shifted) + 1) # амплитудный спектр

    return [image, filtered_image, magnitude_spectrum]

def get_all_info(path):
    image, filtered_image, magnitude_spectrum = get_fourie(path)

    # ВИЗУАЛИЗАЦИЯ
    # исходное изображение
    plt.subplot(1, 3, 1), plt.imshow(image, cmap='gray')
    plt.title('Оригинал'), plt.axis('off')
    # фильтрация частот
    plt.subplot(1, 3, 2), plt.imshow(filtered_image, cmap='gray')
    plt.title('Высокочастотная фильтрация'), plt.axis('off')
    # амплитудные спектр
    plt.subplot(1, 3, 3), plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Амплитудный спектр'), plt.axis('off')

    plt.show()

def get_magnitude(path):
    spectrum = get_fourie(path)[2]
    plt.imshow(spectrum, cmap='gray')
    plt.axis('off')
    plt.gca().set_position([0, 0, 1, 1])
    plt.show()




# get_all_info(r"D:\_git\composition\transforms\6.jpg")
get_magnitude(r"D:\_git\composition\transforms\12.jpg")
