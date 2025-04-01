import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import models


def load_images_from_folder(folder : str) -> list:
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = Image.open(os.path.join(folder, filename))
            if img is not None:
                images.append((filename, img))
    return images

images = load_images_from_folder('processed_images')

for i, (filename, values) in enumerate(images):
    src_x = np.linspace(0, 1, np.array(values).shape[1])
    src_y = np.linspace(0, 1, np.array(values).shape[0])
    tgt_x = np.linspace(0, 1, np.array(values).shape[1] * 2)
    tgt_y = np.linspace(0, 1, np.array(values).shape[0] * 2)

    bilinear_result = models.bilinear_interpolation(src_x, src_y, np.array(values), tgt_x, tgt_y)
    bicubic_result = models.bicubic_interpolation(src_x, src_y, np.array(values), tgt_x, tgt_y)

    # Convert the original image to RGB for the neural network upscale
    original_image = values.convert('RGB')
    
    nn_upscale_result = models.esrgan_interpolation(original_image)

    # Загрузка ground truth
    gt_image_path = os.path.join('processed_images_gt', filename)
    gt_image = Image.open(gt_image_path)
    gt_image_array = np.array(gt_image)

    bilinear_diff = np.abs(bilinear_result - gt_image_array / 256)
    bicubic_diff = np.abs(bicubic_result - gt_image_array / 256)
    nn_upscale_diff = np.abs(nn_upscale_result - gt_image_array)
    bilinear_diff = bilinear_diff / np.quantile(bilinear_diff, 0.95)
    bicubic_diff = bicubic_diff / np.quantile(bicubic_diff, 0.95)
    nn_upscale_diff = nn_upscale_diff / np.quantile(nn_upscale_diff, 0.95)

    fig, axs = plt.subplots(2, 4, figsize=(14, 7))
    fig.canvas.manager.window.wm_geometry("+0+0")

    axs[0, 0].imshow(values, extent=(0, 1, 0, 1), origin='lower')
    axs[0, 0].set_title(f'Input {i+1}')

    axs[0, 1].imshow(np.clip(bilinear_result, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[0, 1].set_title('Bilinear')

    axs[0, 2].imshow(np.clip(bicubic_result, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[0, 2].set_title('Bicubic')

    axs[0, 3].imshow(nn_upscale_result, extent=(0, 1, 0, 1), origin='lower')
    axs[0, 3].set_title('RealESRGAN')


    axs[1, 0].imshow(gt_image, extent=(0, 1, 0, 1), origin='lower')
    axs[1, 0].set_title('Ground Truth')

    # Карты разности
    axs[1, 1].imshow(np.clip(bilinear_diff, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[1, 1].set_title(f'Bilinear Diff, L2norm: {np.linalg.norm(bilinear_diff):.2f}')

    axs[1, 2].imshow(np.clip(bicubic_diff, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[1, 2].set_title(f'Bicubic Diff, L2norm: {np.linalg.norm(bicubic_diff):.2f}')

    axs[1, 3].imshow(np.clip(nn_upscale_diff, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[1, 3].set_title(f'GAN Diff, L2norm: {np.linalg.norm(nn_upscale_diff):.2f}')

    plt.show()
