import timeit
import matplotlib.pyplot as plt

'''
Для примера
'''

import cProfile
import pstats

def profile_join_performance():
    """Профилируем разные методы объединения строк."""
    pr = cProfile.Profile()
    pr.enable()

    # Тестируемый код
    for _ in range(10_000):
        '-'.join(map(str, range(100)))
    
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumtime')  # Сортируем по общему времени
    stats.dump_stats("../docs/_static/join_profile.prof")  # Сохраняем для анализа


def benchmark_join_variants():
    """Тестируем разные способы объединения строк."""
    variants = {
        "List comprehension + join": "'-'.join([str(n) for n in range(100)])",
        "Generator + join": "'-'.join(str(n) for n in range(100))",
        "Map + join": "'-'.join(map(str, range(100)))",
    }

    results = {}
    for name, code in variants.items():
        time = timeit.timeit(code, number=10_000)
        results[name] = time

    return results

def plot_results(results):
    """Строим график по результатам."""
    names = list(results.keys())
    times = list(results.values())

    plt.figure(figsize=(10, 5))
    plt.bar(names, times, color=['skyblue', 'lightgreen', 'salmon'])
    plt.title("Сравнение производительности методов объединения строк")
    plt.ylabel("Время (секунды, 10k итераций)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("../docs/_static/join_performance.png")

if __name__ == "__main__":
    results = benchmark_join_variants()
    profile_join_performance()
    print(results)
    plot_results(results)