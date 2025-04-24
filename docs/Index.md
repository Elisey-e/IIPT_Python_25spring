# Добро пожаловать в Image Upscale/Interpolation Visualisation

**ImgVisInt** — это инструмент для визуализации и анализа различных методов интерполяции и увеличения изображений. Он поддерживает билинейную, бикубическую интерполяцию, а также современные нейросетевые подходы, такие как RealESRGAN. Этот проект создан для демонстрации производительности и качества различных методов обработки изображений.

## Возможности

- **Сравнение методов интерполяции**: билинейная, бикубическая интерполяция и нейросетевые модели.
- **Анализ производительности**: измерение времени выполнения и масштабируемости методов.
- **Визуализация результатов**: графики, таблицы и изображения для наглядного сравнения.

## Быстрый старт

Убедитесь, что у вас установлен Python и Poetry. Затем выполните следующие команды:

### Установка зависимостей

```bash
poetry install
```

### Запуск проекта

**Windows:**

```bash
python transform.py --size 100 100 --input images
python interpolation.py
```

**Linux:**

```bash
poetry install
poetry run python src/imgvisint/transform.py --size 100 100 --input images
poetry run python src/imgvisint/interpolation.py
```

### Пример использования

```python
from imgvisint import bicubic_interpolation, neural_network_upscale
Big_Image = bicubic_interpolation(image, ...)
Big_Image = neural_network_upscale(image, ...)
```

### Пример вывода

![alt text](https://sun9-42.userapi.com/impg/V4C16fI6WiLlIUe_f4NeBox44qA_70mNi9rceg/YlIBnjFEMUI.jpg?size=1400x700&quality=95&sign=fd6cb478dadda401087057ae503eebaf&type=album)

## Содержание документации

```{toctree}
:titlesonly:
:maxdepth: 2

Reference
Licence
apidocs/models/models
Perf
Profiling
```

## Обратная связь

Если у вас есть вопросы или предложения, пожалуйста, создайте issue в [репозитории проекта](https://github.com/Elisey-e/IIPT_Python_25spring).