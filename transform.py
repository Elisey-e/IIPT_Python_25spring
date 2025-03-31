import os
import argparse
from PIL import Image

resize_scale = 2 # Константа для выбранных моделей resize

def crop_and_resize(image_path, output_path, size=(100, 100)):
    """Вырезает квадратную часть изображения и изменяет размер до 100x100."""
    with Image.open(image_path) as img:
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2

        img_cropped = img.crop((left, top, right, bottom))
        img_resized = img_cropped.resize(size, Image.LANCZOS)
        output_path = os.path.splitext(output_path)[0] + '.png'
        img_resized.save(output_path, 'PNG')

def process_images(input_dir, output_dir, size):
    """Проходит по всем изображениям в директории и обрабатывает их."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')
            crop_and_resize(input_path, output_path, size=size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Обработка изображений: обрезка и изменение размера')
    parser.add_argument('--size', type=int, nargs=2, default=[100, 100],
                        help='Размер выходного изображения (ширина высота), например: 100 100')
    parser.add_argument('--input', type=str, default='images',
                        help='Входная директория с изображениями (по умолчанию: images)')
    
    args = parser.parse_args()
    
    process_images(args.input, 'processed_images', tuple(args.size))
    process_images(args.input, 'processed_images_gt', (args.size[0] * 2, args.size[1] * 2))