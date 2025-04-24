"""
Модуль для повышения разрешения изображений с использованием нейросетевой модели RealESRGAN.

Модуль предоставляет функционал для апскейла (увеличения разрешения) изображений
в 2 раза с сохранением и улучшением детализации с помощью предобученной модели RealESRGAN.

Требуемые библиотеки:
- numpy
- torch
- PIL
- RealESRGAN
"""

import numpy as np
import torch
from PIL import Image
from RealESRGAN import RealESRGAN

# Определение устройства для вычислений (GPU если доступно, иначе CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Инициализация модели RealESRGAN с масштабом увеличения 2x
model = RealESRGAN(device, scale=2)

# Загрузка весов модели. Если веса отсутствуют, они будут автоматически загружены
model.load_weights("weights/RealESRGAN_x2.pth", download=True)


def neural_network_upscale(image: Image.Image) -> np.ndarray:
    """
    Увеличивает разрешение входного изображения в 2 раза с помощью модели RealESRGAN.

    Параметры:
    ----------
    image : PIL.Image.Image
        Входное изображение для апскейла. Может быть в любом формате, поддерживаемом PIL.

    Возвращает:
    ----------
    np.ndarray
        Массив NumPy с увеличенным изображением в формате (H, W, C),
        где H - высота, W - ширина, C - количество цветовых каналов (обычно 3 для RGB).

    Примеры:
    --------
    >>> from PIL import Image
    >>> image = Image.open("input.jpg")
    >>> upscaled_image = neural_network_upscale(image)
    >>> Image.fromarray(upscaled_image).save("output.jpg")

    Примечания:
    ----------
    - Модель RealESRGAN особенно эффективна для восстановления деталей в фотографиях
      и изображениях с артефактами сжатия.
    - Для работы функции требуется доступ к GPU для оптимальной производительности,
      хотя возможно выполнение и на CPU (значительно медленнее).
    - Функция автоматически конвертирует изображение в формат, подходящий для модели.
    """
    # Выполнение предсказания (апскейла изображения)
    sr_image = model.predict(image)
    
    # Конвертация результата в массив NumPy и возврат
    return np.array(sr_image)