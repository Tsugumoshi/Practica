"""Скоростные замеры и диагностика памяти (timeit, cProfile, tracemalloc).

Запуск из каталога репозитория:
    python profiling/run_benchmarks.py
"""

import cProfile
import io
import pstats
import sys
import timeit
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_program import (  # noqa: E402
    fib_iterative,
    fib_recursive,
    matrix_multiply,
    memory_churn,
    sieve_of_eratosthenes,
)


def run_timeit() -> None:
    """Точечные замеры скорости функцией timeit."""
    print("=" * 70)
    print("1. TIMEIT — среднее время одного вызова")
    print("=" * 70)
    cases = [
        ("fib_recursive(30)", "fib_recursive(30)", 5),
        ("fib_iterative(10000)", "fib_iterative(10000)", 100),
        ("matrix_multiply(200)", "matrix_multiply(200)", 10),
        ("sieve_of_eratosthenes(100000)", "sieve_of_eratosthenes(100000)", 10),
        ("memory_churn()", "memory_churn()", 100),
    ]
    setup = "from demo_program import fib_recursive, fib_iterative, matrix_multiply, sieve_of_eratosthenes, memory_churn"
    for name, stmt, number in cases:
        total = timeit.timeit(stmt, setup=setup, number=number)
        avg_us = total / number * 1_000_000
        print(f"{name:32s} {avg_us:14.2f} мкс/вызов  ({number} прогонов, {total:.4f} с)")


def run_cprofile() -> None:
    """Общая картина выполнения функцией cProfile."""
    print()
    print("=" * 70)
    print("2. CPROFILE — функция fib_recursive(30)")
    print("=" * 70)
    profiler = cProfile.Profile()
    profiler.enable()
    fib_recursive(30)
    profiler.disable()
    out = io.StringIO()
    stats = pstats.Stats(profiler, stream=out)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(5)
    text = out.getvalue()
    for line in text.splitlines():
        if "fib_recursive" in line or "function calls" in line:
            print(line.strip())


def run_tracemalloc() -> None:
    """Снимки памяти функцией tracemalloc."""
    print()
    print("=" * 70)
    print("3. TRACEMALLOC — снимки памяти для memory_churn()")
    print("=" * 70)
    tracemalloc.start()
    before = tracemalloc.take_snapshot()
    for _ in range(50):
        memory_churn()
    after = tracemalloc.take_snapshot()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Текущее потребление: {current / 1024:.2f} KiB; пик: {peak / 1024:.2f} KiB")
    print("Топ-3 по приросту памяти:")
    for stat in after.compare_to(before, "lineno")[:3]:
        print(f"  {stat}")


if __name__ == "__main__":
    run_timeit()
    run_cprofile()
    run_tracemalloc()
