"""Сравнение пяти алгоритмов сортировки."""
from __future__ import annotations

import random
import time
import csv
from pathlib import Path
from typing import Callable


def bubble_sort(data: list[int]) -> list[int]:
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(data: list[int]) -> list[int]:
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def insertion_sort(data: list[int]) -> list[int]:
    arr = data.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def quick_sort(data: list[int]) -> list[int]:
    arr = data.copy()

    def sort_range(left: int, right: int) -> None:
        i, j = left, right
        pivot = arr[(left + right) // 2]
        while i <= j:
            while arr[i] < pivot:
                i += 1
            while arr[j] > pivot:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        if left < j:
            sort_range(left, j)
        if i < right:
            sort_range(i, right)

    if arr:
        sort_range(0, len(arr) - 1)
    return arr


def merge_sort(data: list[int]) -> list[int]:
    if len(data) <= 1:
        return data.copy()
    middle = len(data) // 2
    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


ALGORITHMS: dict[str, Callable[[list[int]], list[int]]] = {
    "Пузырьковая сортировка": bubble_sort,
    "Сортировка выбором": selection_sort,
    "Сортировка вставками": insertion_sort,
    "Быстрая сортировка": quick_sort,
    "Сортировка слиянием": merge_sort,
}


def read_array() -> list[int]:
    print("\nКак задать массив?")
    print("1 — ввести числа вручную")
    print("2 — сгенерировать случайный массив")
    choice = input("Ваш выбор: ").strip()
    if choice == "1":
        while True:
            raw = input("Введите целые числа через пробел: ").strip()
            try:
                values = [int(item) for item in raw.split()]
                if not values:
                    raise ValueError
                return values
            except ValueError:
                print("Ошибка: введите хотя бы одно целое число, разделяя числа пробелами.")
    while True:
        try:
            size = int(input("Количество элементов (1–100): "))
            if 1 <= size <= 100:
                return [random.randint(-99, 99) for _ in range(size)]
        except ValueError:
            pass
        print("Введите целое число от 1 до 100.")


def show_sorting(data: list[int], names: list[str]) -> None:
    print("\nИсходный массив:")
    print(data)
    for name in names:
        start = time.perf_counter()
        result = ALGORITHMS[name](data)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"\n{name}:")
        print("До:    ", data)
        print("После: ", result)
        print(f"Время выполнения: {elapsed_ms:.4f} мс")
        if result != sorted(data):
            print("Ошибка! результат не совпал с эталонной сортировкой!")


def demonstrate_steps(data: list[int], name: str) -> list[int]:
    """Пошагово показывает основные действия выбранного алгоритма."""
    arr = data.copy()
    step_no = 0

    def show(action: str, state: list[int] | None = None) -> None:
        nonlocal step_no
        step_no += 1
        print(f"Шаг {step_no}: {action}")
        if state is not None:
            print("   Массив:", state)

    print(f"\nПошаговая демонстрация: {name}")
    print("Исходный массив:", arr)

    if name == "Пузырьковая сортировка":
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                show(f"сравниваем {arr[j]} и {arr[j + 1]}")
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    show("элементы поменялись местами", arr)
            if not swapped:
                show("за проход перестановок нет - сортировка завершена")
                break

    elif name == "Сортировка выбором":
        for i in range(len(arr)):
            min_index = i
            for j in range(i + 1, len(arr)):
                show(f"ищем минимум: сравниваем {arr[j]} и текущий минимум {arr[min_index]}")
                if arr[j] < arr[min_index]:
                    min_index = j
            if min_index != i:
                arr[i], arr[min_index] = arr[min_index], arr[i]
                show(f"минимум {arr[i]} ставим на позицию {i}", arr)
            else:
                show(f"элемент {arr[i]} уже находится на нужной позиции", arr)

    elif name == "Сортировка вставками":
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            show(f"вставляем элемент {key} в отсортированную левую часть")
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                show(f"сдвигаем элемент вправо", arr)
            arr[j + 1] = key
            show(f"элемент {key} вставлен на позицию {j + 1}", arr)

    elif name == "Быстрая сортировка":
        def partition_sort(left: int, right: int) -> None:
            if left >= right:
                return
            i, j = left, right
            pivot = arr[(left + right) // 2]
            show(f"диапазон [{left}:{right + 1}], опорный элемент = {pivot}", arr)
            while i <= j:
                while arr[i] < pivot:
                    i += 1
                while arr[j] > pivot:
                    j -= 1
                if i <= j:
                    if i != j:
                        arr[i], arr[j] = arr[j], arr[i]
                        show(f"меняем элементы на позициях {i} и {j}", arr)
                    i += 1
                    j -= 1
            if left < j:
                partition_sort(left, j)
            if i < right:
                partition_sort(i, right)
        if arr:
            partition_sort(0, len(arr) - 1)

    elif name == "Сортировка слиянием":
        def merge_sort_trace(part: list[int]) -> list[int]:
            if len(part) <= 1:
                return part.copy()
            middle = len(part) // 2
            left = merge_sort_trace(part[:middle])
            right = merge_sort_trace(part[middle:])
            merged: list[int] = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i]); i += 1
                else:
                    merged.append(right[j]); j += 1
            merged.extend(left[i:]); merged.extend(right[j:])
            show(f"сливаем {left} и {right} → {merged}")
            return merged
        arr = merge_sort_trace(arr)

    print("Итоговый массив:", arr)
    print(f"Всего шагов: {step_no}")
    return arr


def run_benchmark() -> None:
    """Сравнивает время алгоритмов на случайных массивах и сохраняет CSV."""
    sizes = [100, 500, 1000, 2000]
    output_path = Path(__file__).with_name("benchmark_results.csv")
    rows: list[dict[str, object]] = []
    print("\nЭксперимент: случайные массивы, время в миллисекундах")
    print(f"{'Размер':>8}  " + "  ".join(f"{name[:12]:>12}" for name in ALGORITHMS))
    for size in sizes:
        data = [random.randint(-10000, 10000) for _ in range(size)]
        times: list[str] = []
        for name, algorithm in ALGORITHMS.items():
            start = time.perf_counter()
            result = algorithm(data)
            elapsed_ms = (time.perf_counter() - start) * 1000
            assert result == sorted(data), f"Ошибка в алгоритме: {name}"
            rows.append({"Размер массива": size, "Алгоритм": name, "Время, мс": round(elapsed_ms, 4)})
            times.append(f"{elapsed_ms:12.4f}")
        print(f"{size:8d}  " + "  ".join(times))
    with output_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["Размер массива", "Алгоритм", "Время, мс"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nРезультаты сохранены в файл: {output_path.name}")
    print("Время зависит от компьютера и текущей нагрузки; для отчёта повторите эксперимент несколько раз.")


def main() -> None:
    while True:
        print("\nЭволюция алгоритмов сортировки")
        print("1 — пузырьковая сортировка")
        print("2 — сортировка выбором")
        print("3 — сортировка вставками")
        print("4 — быстрая сортировка")
        print("5 — сортировка слиянием")
        print("6 — сравнить все пять алгоритмов на одном массиве")
        print("7 — экспериментальное исследование (CSV)")
        print("8 — пошаговая демонстрация одного алгоритма")
        print("0 — выход")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("Работа программы завершена.")
            break
        if choice == "7":
            run_benchmark()
            continue
        if choice == "8":
            data = read_array()
            print("\nВыберите алгоритм для пошаговой демонстрации:")
            for index, name in enumerate(ALGORITHMS, start=1):
                print(f"{index} — {name}")
            algorithm_choice = input("Ваш выбор: ").strip()
            if algorithm_choice in {"1", "2", "3", "4", "5"}:
                name = list(ALGORITHMS)[int(algorithm_choice) - 1]
                result = demonstrate_steps(data, name)
                if result != sorted(data):
                    print("Ошибка! Результат не совпал с эталонной сортировкой!")
            else:
                print("Нет такого алгоритма.")
            continue
        if choice in {"1", "2", "3", "4", "5", "6"}:
            data = read_array()
            if choice == "6":
                names = list(ALGORITHMS)
            else:
                names = [list(ALGORITHMS)[int(choice) - 1]]
            show_sorting(data, names)
        else:
            print("Нет такого пункта меню. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()