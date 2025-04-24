import os
import sys
import timeit

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir = os.path.abspath(os.path.join(current_dir, "../.."))
if parent_parent_dir not in sys.path:
    sys.path.append(parent_parent_dir)

# Импорт моделей интерполяции
import models


def load_test_image(image_path="test_image.png"):
    """Загрузка или создание тестового RGB изображения"""
    if not os.path.exists(image_path):
        # Создаем тестовое RGB изображение
        arr = np.random.rand(256, 256, 3) * 255
        img = Image.fromarray(arr.astype("uint8"), "RGB")
        img.save(image_path)
        return img
    return Image.open(image_path).convert("RGB")


def benchmark_interpolation_methods(image_size=256, repeats=5):
    """
    Бенчмарк методов интерполяции
    :param image_size: размер тестового изображения
    :param repeats: количество повторений для усреднения
    :return: словарь с результатами
    """
    # Создаем тестовое RGB изображение
    test_img = Image.new("RGB", (image_size, image_size))

    # Подготовка координатных сеток
    src_x = np.linspace(0, 1, image_size)
    src_y = np.linspace(0, 1, image_size)
    tgt_x = np.linspace(0, 1, image_size * 2)
    tgt_y = np.linspace(0, 1, image_size * 2)

    # Настройка окружения для timeit
    setup = f"""
import numpy as np
from PIL import Image
import models
test_img = Image.new('RGB', ({image_size}, {image_size}))
src_x = np.linspace(0, 1, {image_size})
src_y = np.linspace(0, 1, {image_size})
tgt_x = np.linspace(0, 1, {image_size * 2})
tgt_y = np.linspace(0, 1, {image_size * 2})
img_array = np.array(test_img)
    """

    # Тестируемые методы
    methods = {
        "Bilinear": "models.bilinear_interpolation(src_x, src_y, img_array, tgt_x, tgt_y)",
        "Bicubic": "models.bicubic_interpolation(src_x, src_y, img_array, tgt_x, tgt_y)",
        "ESRGAN": "models.esrgan_interpolation(test_img)",
    }

    results = {}
    for name, stmt in methods.items():
        try:
            # Для ESRGAN делаем меньше повторов
            number = max(1, repeats // 3) if name == "ESRGAN" else repeats
            timer = timeit.Timer(stmt=stmt, setup=setup)

            # Для медленных методов уменьшаем количество итераций
            if name == "ESRGAN":
                time_taken = timer.timeit(number=1)
                avg_time = time_taken
                iterations = 1
            else:
                iterations, time_taken = timer.autorange()
                avg_time = time_taken / iterations

            results[name] = {"avg_time": avg_time, "iterations": iterations, "total_time": time_taken}
        except Exception as e:
            print(f"Error benchmarking {name}: {str(e)}")
            results[name] = {"avg_time": float("nan"), "iterations": 0, "total_time": float("nan")}

    return results


def plot_results(results, image_size):
    """Визуализация результатов"""
    # Фильтруем методы с ошибками
    valid_results = {k: v for k, v in results.items() if not np.isnan(v["avg_time"])}

    if not valid_results:
        print("No valid results to plot!")
        return

    methods = list(valid_results.keys())
    times = [valid_results[m]["avg_time"] for m in methods]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(methods, times, color=["blue", "green", "red"])

    # Добавляем значения на столбцы
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{height:.4f}s", ha="center", va="bottom")

    plt.ylabel("Average Execution Time (seconds)")
    plt.title(f"Interpolation Methods Performance Comparison\nImage size: {image_size}x{image_size}")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.yscale("log")
    plt.tight_layout()

    # Сохраняем график
    plot_path = "docs/_static/interpolation_performance.png"
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")


if __name__ == "__main__":
    # Параметры бенчмарка
    IMAGE_SIZE = 256  # Размер тестового изображения
    REPEATS = 10  # Количество повторений для усреднения

    print(f"Running benchmark for {IMAGE_SIZE}x{IMAGE_SIZE} image...")
    results = benchmark_interpolation_methods(IMAGE_SIZE, REPEATS)

    # Вывод результатов
    print("\nBenchmark Results:")
    for method, data in results.items():
        if np.isnan(data["avg_time"]):
            print(f"{method}: Failed to benchmark")
        else:
            print(f"{method}: {data['avg_time']:.6f} sec per iteration (averaged over {data['iterations']} runs)")

    # Визуализация
    plot_results(results, IMAGE_SIZE)
