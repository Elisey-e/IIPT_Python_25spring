import numpy as np
import scipy.interpolate as interp


def bilinear_interpolation(x : list, y : list, values : list, xi : list, yi : list) -> np.stack:
    """Билинейная интерполяция значений на новой сетке для цветного изображения."""
    channels = []
    for i in range(values.shape[2]):
        f = interp.interp2d(x, y, values[:, :, i], kind='linear')
        channels.append(f(xi, yi))
    return np.stack(channels, axis=-1) / 256