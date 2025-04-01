import numpy as np
import pytest

import models


@pytest.mark.parametrize("sz", [
    10, 100, 1000
])

def test_bicubic_zeros(sz : int) -> None:
    values = np.zeros((sz, sz, 3))
    src_x = np.linspace(0, 1, np.array(values).shape[1])
    src_y = np.linspace(0, 1, np.array(values).shape[0])
    tgt_x = np.linspace(0, 1, np.array(values).shape[1] * 2)
    tgt_y = np.linspace(0, 1, np.array(values).shape[0] * 2)

    bicubic_result = models.bicubic_interpolation(src_x, src_y, np.array(values), tgt_x, tgt_y)
    assert np.allclose(bicubic_result, np.zeros((sz * 2, sz * 2, 3)))



@pytest.mark.parametrize("sz", [
    10, 100, 1000
])

def test_bicubic_noise(sz : int) -> None:
    values = np.random.randn(sz, sz, 3)
    src_x = np.linspace(0, 1, np.array(values).shape[1])
    src_y = np.linspace(0, 1, np.array(values).shape[0])
    tgt_x = np.linspace(0, 1, np.array(values).shape[1] * 2)
    tgt_y = np.linspace(0, 1, np.array(values).shape[0] * 2)

    bicubic_result = models.bicubic_interpolation(src_x, src_y, np.array(values), tgt_x, tgt_y)
    assert abs(np.mean(bicubic_result)) < 0.001



def test_bicubic_izo() -> None:
    gradient = np.linspace(1, 0, 100)
    values = gradient[:, np.newaxis, np.newaxis] * np.ones((100, 100, 3))
    
    gradient = np.linspace(1, 0, 200)
    ans_x2 = gradient[:, np.newaxis, np.newaxis] * np.ones((200, 200, 3))

    src_x = np.linspace(0, 1, np.array(values).shape[1])
    src_y = np.linspace(0, 1, np.array(values).shape[0])
    tgt_x = np.linspace(0, 1, np.array(values).shape[1] * 2)
    tgt_y = np.linspace(0, 1, np.array(values).shape[0] * 2)

    bicubic_result = models.bicubic_interpolation(src_x, src_y, np.array(values), tgt_x, tgt_y)
    assert np.allclose(bicubic_result * 256, ans_x2)
