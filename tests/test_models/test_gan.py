import numpy as np
import pytest
from PIL import Image

import models

"""
Замечание: присутствуют статистические оценки, средняя срабатываемость тестов около 2 sigma 
"""


@pytest.mark.parametrize("sz", [
    20, 50, 100, 200
])

def test_gan_zeros(sz : int) -> None:
    values = np.zeros((sz, sz, 3), dtype=np.uint8)
    values = Image.fromarray(values)
    original_image = values.convert('RGB')
    

    res = models.esrgan_interpolation(original_image)
    assert np.allclose(res, np.zeros((sz * 2, sz * 2, 3), dtype=np.uint8))


@pytest.mark.parametrize("sz", [
    20, 50, 100, 200
])

def test_gan_noise(sz : int) -> None:
    values = np.random.randint(0, 255, (sz, sz, 3), dtype=np.uint8)
    values = Image.fromarray(values)
    original_image = values.convert('RGB')
    

    res = models.esrgan_interpolation(original_image)
    assert 128 - 128 ** 0.5 < abs(np.mean(res)) < 128 + 128 ** 0.5


def test_gan_izo() -> None:
    gradient = np.array(list(range(0, 254, 2)))
    values = np.round(gradient[:, np.newaxis, np.newaxis] * np.ones((127, 127, 3)) * 253 / 252)
    values = values.astype(np.uint8)
    
    gradient = np.array(list(range(0, 254, 1)))
    ans_x2 = gradient[:, np.newaxis, np.newaxis] * np.ones((254, 254, 3))
    ans_x2 = ans_x2.astype(np.uint8)

    values = Image.fromarray(values)
    values = values.convert('RGB')

    ans_x2 = Image.fromarray(ans_x2)
    ans_x2 = ans_x2.convert('RGB')

    res = models.esrgan_interpolation(values)


    assert np.max(np.abs(np.array(res).astype(np.float32) - np.array(ans_x2).astype(np.float32))) < 128 ** 0.5
