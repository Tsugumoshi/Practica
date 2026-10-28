"""Построчный анализ потребления памяти (memory_profiler).

Запуск из каталога репозитория:
    python -m memory_profiler profiling/mem_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_program import (  # noqa: E402
    matrix_multiply,
    memory_churn,
    sieve_of_eratosthenes,
)


@profile  # noqa: F821 — определяется memory_profiler
def workload():
    """Три функции с разным потреблением памяти."""
    matrix_multiply(200)
    sieve_of_eratosthenes(100000)
    memory_churn()


if __name__ == "__main__":
    workload()
