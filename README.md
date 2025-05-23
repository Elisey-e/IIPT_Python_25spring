# Домашние задания по курсу "Программирование на питон" ИППИ РАН

Жданов Елисей

## Описание проекта

Проект посвящен визуализации методов интерполяции изображений. Включает в себя реализацию и анализ различных моделей интерполяции, таких как билинейная, бикубическая интерполяция и ESRGAN (Enhanced Super-Resolution Generative Adversarial Network).

## Установка и запуск

Конфигурационные файлы в папке configs, используйте их в корне проекта

### Windows

```bash
git clone https://github.com/Elisey-e/IIPT_Python_25spring.git
cd IIPT_Python_25spring
git clone https://github.com/ai-forever/Real-ESRGAN.git
poetry install
run.bat
```

### Linux

```bash
git clone https://github.com/Elisey-e/IIPT_Python_25spring.git
cd IIPT_Python_25spring
git clone https://github.com/ai-forever/Real-ESRGAN.git
poetry install
bash run.sh
```

## Пример вывода

![Пример вывода](https://sun9-42.userapi.com/impg/V4C16fI6WiLlIUe_f4NeBox44qA_70mNi9rceg/YlIBnjFEMUI.jpg?size=1400x700&quality=95&sign=fd6cb478dadda401087057ae503eebaf&type=album)

## Запуск nox сессии

```bash
nox
```


## Модели

1. **Билинейная интерполяция**  
    Простая модель интерполяции, использующая линейное усреднение соседних пикселей.  
    Формула для билинейной интерполяции:  

    ```
    f(x, y) = f(x1, y1) * (1 - dx) * (1 - dy) + 
              f(x2, y1) * dx * (1 - dy) + 
              f(x1, y2) * (1 - dx) * dy + 
              f(x2, y2) * dx * dy
    ```

    где `dx = x - x1`, `dy = y - y1`.

2. **Бикубическая интерполяция**  
    Более сложная модель, использующая кубические сплайны для интерполяции.  
    Формула для бикубической интерполяции:  

    ```
    f(x, y) = Σ Σ w(i, j) * f(xi, yj)
    ```

    где `w(i, j)` — весовая функция, зависящая от расстояния до соседних точек.

3. **ESRGAN (Enhanced Super-Resolution GAN)**  
    Генеративно-состязательная сеть для увеличения разрешения изображений.  
    ESRGAN использует архитектуру GAN для восстановления высокодетализированных изображений из низкого разрешения, обучаясь на парах изображений высокого и низкого качества.

## Документация

Подробная документация доступна в папке `docs`. Основные разделы:

- [Reference](docs/_build/html/Reference.html) — описание API.
- [Perf analysis](docs/_build/html/Perf.html) — анализ производительности.
- [Profiling](docs/_build/html/Profiling.html) — профилирование моделей.
- [API Reference](docs/_build/html/apidocs/index.html) — автогенерированная документация API.

## Обратная связь

Если у вас есть вопросы или предложения, создайте issue в [репозитории проекта](https://github.com/Elisey-e/IIPT_Python_25spring).