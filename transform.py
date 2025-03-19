import os
from PIL import Image

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
    input_directory = 'images'
    output_directory = 'processed_images'
    process_images(input_directory, output_directory, size=(100, 100))

    output_directory = 'processed_images_gt'
    process_images(input_directory, output_directory, size=(200, 200))
