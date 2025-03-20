import scipy.interpolate as interp
import numpy as np


def bilinear_interpolation(x, y, values, xi, yi):
    """Билинейная интерполяция значений на новой сетке для цветного изображения."""
    channels = []
    for i in range(values.shape[2]):
        f = interp.interp2d(x, y, values[:, :, i], kind='linear')
        channels.append(f(xi, yi))
    return np.stack(channels, axis=-1) / 256