import os
import sys
import timeit
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir = os.path.abspath(os.path.join(current_dir, '../..'))
if parent_parent_dir not in sys.path:
    sys.path.append(parent_parent_dir)

# Импорт моделей интерполяции
import models

def create_test_image(size, channels=3):
    """Создание тестового RGB изображения заданного размера"""
    if channels == 1:
        arr = np.random.rand(size, size) * 255
        return Image.fromarray(arr.astype('uint8'), 'L')
    else:
        arr = np.random.rand(size, size, 3) * 255
        return Image.fromarray(arr.astype('uint8'), 'RGB')

def benchmark_for_size(image_size, repeats=3):
    """
    Замер времени для одного размера изображения
    :param image_size: размер изображения
    :param repeats: количество повторений
    :return: словарь с результатами
    """
    # Настройка окружения для timeit
    setup = f"""
import numpy as np
from PIL import Image
import models
from __main__ import create_test_image
test_img = create_test_image({image_size})
src_x = np.linspace(0, 1, {image_size})
src_y = np.linspace(0, 1, {image_size})
tgt_x = np.linspace(0, 1, {image_size*2})
tgt_y = np.linspace(0, 1, {image_size*2})
img_array = np.array(test_img)
if len(img_array.shape) == 2:
    img_array = np.expand_dims(img_array, axis=-1)
    """
    
    methods = {
        'Bilinear': 'models.bilinear_interpolation(src_x, src_y, img_array, tgt_x, tgt_y)',
        'Bicubic': 'models.bicubic_interpolation(src_x, src_y, img_array, tgt_x, tgt_y)',
        'ESRGAN': 'models.esrgan_interpolation(test_img)'
    }
    
    results = {}
    for name, stmt in methods.items():
        try:
            # Для ESRGAN делаем только 1 повторение
            number = 1 if name == 'ESRGAN' else repeats
            
            timer = timeit.Timer(stmt=stmt, setup=setup)
            
            if name == 'ESRGAN':
                time_taken = timer.timeit(number=1)
                avg_time = time_taken
            else:
                time_taken = timer.timeit(number=number)
                avg_time = time_taken / number
            
            results[name] = avg_time
        except Exception as e:
            print(f"Error benchmarking {name} at size {image_size}: {str(e)}")
            results[name] = np.nan
    
    return results

def plot_size_dependency(results, sizes):
    """Построение графика зависимости времени от размера изображения"""
    methods = list(results[sizes[0]].keys())
    colors = {'Bilinear': 'blue', 'Bicubic': 'green', 'ESRGAN': 'red'}
    
    plt.figure(figsize=(12, 7))
    
    for method in methods:
        times = []
        valid_sizes = []
        
        for size in sizes:
            time_val = results[size].get(method, np.nan)
            if not np.isnan(time_val):
                times.append(time_val)
                valid_sizes.append(size)
        
        if valid_sizes:
            plt.plot(valid_sizes, times, 
                    label=method, 
                    color=colors.get(method, 'black'),
                    marker='o',
                    linestyle='-')
    
    plt.xlabel('Image Size (pixels)')
    plt.ylabel('Time (seconds)')
    plt.title('Interpolation Time vs Image Size')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    # Добавляем размеры на ось X
    plt.xticks(sizes, [str(size) for size in sizes])
    
    plt.tight_layout()
    
    # Сохраняем график
    plot_path = 'docs/_static/interpolation_size_scaling.png'
    plt.savefig(plot_path)
    plt.show()
    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    # Размеры изображений для тестирования
    IMAGE_SIZES = [16, 32, 64, 128, 256, 512, 1024, 2048]  # Можно добавить больше размеров
    REPEATS = 5  # Количество повторений для каждого размера
    
    print("Running benchmark for different image sizes...")
    
    results = {}
    for size in IMAGE_SIZES:
        print(f"\nBenchmarking size {size}x{size}...")
        results[size] = benchmark_for_size(size, REPEATS)
        
        # Вывод промежуточных результатов
        print(f"Results for {size}x{size}:")
        for method, time_val in results[size].items():
            if np.isnan(time_val):
                print(f"  {method}: Failed")
            else:
                print(f"  {method}: {time_val:.4f} sec")
    
    # Визуализация
    plot_size_dependency(results, IMAGE_SIZES)
    
    # Сохранение результатов в файл
    import json
    with open('docs/_static/benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Results saved to benchmark_results.json")