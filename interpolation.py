import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import os
from PIL import Image
import torch
from RealESRGAN import RealESRGAN
from super_image import EdsrModel, ImageLoader

def bilinear_interpolation(x, y, values, xi, yi):
    """Билинейная интерполяция значений на новой сетке для цветного изображения."""
    channels = []
    for i in range(values.shape[2]):
        f = interp.interp2d(x, y, values[:, :, i], kind='linear')
        channels.append(f(xi, yi))
    return np.stack(channels, axis=-1) / 256

def bicubic_interpolation(x, y, values, xi, yi):
    """Бикубическая интерполяция значений на новой сетке для цветного изображения."""
    channels = []
    for i in range(values.shape[2]):
        f = interp.interp2d(x, y, values[:, :, i], kind='cubic')
        channels.append(f(xi, yi))
    return np.stack(channels, axis=-1) / 256

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = Image.open(os.path.join(folder, filename))
            if img is not None:
                images.append((filename, img))
    return images

def neural_network_upscale(image, model):
    """Upscale image using RealESRGAN model."""
    sr_image = model.predict(image)
    return np.array(sr_image)

# Initialize RealESRGAN model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = RealESRGAN(device, scale=2)
model.load_weights('weights/RealESRGAN_x2.pth', download=True)

# Загрузка изображений из папки
images = load_images_from_folder('processed_images')

# Обработка каждого изображения
for i, (filename, values) in enumerate(images):
    src_x = np.linspace(0, 1, np.array(values).shape[1])
    src_y = np.linspace(0, 1, np.array(values).shape[0])
    tgt_x = np.linspace(0, 1, np.array(values).shape[1] * 2)
    tgt_y = np.linspace(0, 1, np.array(values).shape[0] * 2)

    bilinear_result = bilinear_interpolation(src_x, src_y, np.array(values)[:, :, :], tgt_x, tgt_y)
    bicubic_result = bicubic_interpolation(src_x, src_y, np.array(values)[:, :, :], tgt_x, tgt_y)

    # Convert the original image to RGB for the neural network upscale
    original_image = values.convert('RGB')
    
    nn_upscale_result = neural_network_upscale(original_image, model)

    # Загрузка увеличенного изображения из папки processed_images_gt
    gt_image_path = os.path.join('processed_images_gt', filename)
    gt_image = Image.open(gt_image_path)
    gt_image_array = np.array(gt_image)

    # Вычисление разностных изображений
    bilinear_diff = np.abs(bilinear_result - gt_image_array / 256)
    bicubic_diff = np.abs(bicubic_result - gt_image_array / 256)
    nn_upscale_diff = np.abs(nn_upscale_result - gt_image_array)
    bilinear_diff = bilinear_diff / np.quantile(bilinear_diff, 0.95)
    bicubic_diff = bicubic_diff / np.quantile(bicubic_diff, 0.95)
    nn_upscale_diff = nn_upscale_diff / np.quantile(nn_upscale_diff, 0.95)

    # Построение графиков
    fig, axs = plt.subplots(2, 4, figsize=(14, 7))
    fig.canvas.manager.window.wm_geometry("+0+0")

    # Исходные данные
    axs[0, 0].imshow(values, extent=(0, 1, 0, 1), origin='lower')
    axs[0, 0].set_title(f'Input {i+1}')

    # Билинейная интерполяция
    axs[0, 1].imshow(np.clip(bilinear_result, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[0, 1].set_title('Bilinear')

    # Бикубическая интерполяция
    axs[0, 2].imshow(np.clip(bicubic_result, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[0, 2].set_title('Bicubic')

    # Нейросетевая интерполяция (RealESRGAN)
    axs[0, 3].imshow(nn_upscale_result, extent=(0, 1, 0, 1), origin='lower')
    axs[0, 3].set_title('RealESRGAN')

    # Увеличенное изображение из папки processed_images_gt
    axs[1, 0].imshow(np.clip(gt_image, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[1, 0].set_title('Ground Truth')

    # Карты разности
    axs[1, 1].imshow(np.clip(bilinear_diff, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[1, 1].set_title(f'Bilinear Diff, L2norm: {np.linalg.norm(bilinear_diff):.2f}')

    axs[1, 2].imshow(np.clip(bicubic_diff, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[1, 2].set_title(f'Bicubic Diff, L2norm: {np.linalg.norm(bicubic_diff):.2f}')

    axs[1, 3].imshow(np.clip(nn_upscale_diff, 0, 1), extent=(0, 1, 0, 1), origin='lower')
    axs[1, 3].set_title(f'GAN Diff, L2norm: {np.linalg.norm(nn_upscale_diff):.2f}')

    plt.show()
