"""Экспериментальный бенчмарк для проекта сортировок.
Запускать рядом с main.py: python3 benchmark_experiment.py
"""
from __future__ import annotations
import csv
import random
import statistics
import time
from pathlib import Path

from main import bubble_sort, selection_sort, insertion_sort, quick_sort, merge_sort

BASE_DIR = Path(__file__).resolve().parent
ALGORITHMS = {
    "Пузырьковая сортировка": bubble_sort,
    "Сортировка выбором": selection_sort,
    "Сортировка вставками": insertion_sort,
    "Быстрая сортировка": quick_sort,
    "Сортировка слиянием": merge_sort,
}
SIZES = (100, 1000, 10000)
DATA_TYPES = ("Случайный", "Отсортированный", "Обратный")
REPEATS = 1


def make_array(size: int, data_type: str, seed: int) -> list[int]:
    rng = random.Random(seed)
    values = [rng.randint(-size * 2, size * 2) for _ in range(size)]
    if data_type == "Отсортированный":
        return sorted(values)
    if data_type == "Обратный":
        return sorted(values, reverse=True)
    return values


def main() -> None:
    output = BASE_DIR / "benchmark_results.csv"
    rows = []
    for size in SIZES:
        for data_type in DATA_TYPES:
            data = make_array(size, data_type, seed=20261025 + size)
            expected = sorted(data)
            for algorithm_name, algorithm in ALGORITHMS.items():
                samples_ms = []
                for _ in range(REPEATS):
                    start = time.perf_counter()
                    result = algorithm(data)
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    if result != expected:
                        raise AssertionError(f"Ошибка сортировки: {algorithm_name}, {size}, {data_type}")
                    samples_ms.append(elapsed_ms)
                rows.append({
                    "algorithm": algorithm_name,
                    "size": size,
                    "data_type": data_type,
                    "repeats": REPEATS,
                    "time_ms_mean": round(statistics.mean(samples_ms), 6),
                    "time_ms_min": round(min(samples_ms), 6),
                    "time_ms_max": round(max(samples_ms), 6),
                    "correct": True,
                })
                print(f"{size:>5} | {data_type:<16} | {algorithm_name:<27} | {statistics.mean(samples_ms):>10.3f} ms")
    with output.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nГотово: {output}")
    print(f"Записей: {len(rows)}; каждый сценарий повторён {REPEATS} раза.")

if __name__ == "__main__":
    main()