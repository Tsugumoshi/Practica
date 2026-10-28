"""Сценарий для Scalene: одновременный замер CPU и памяти.

Запуск из каталога репозитория:
    scalene profiling/scalene_demo.py --outfile profiling/scalene_report.html
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_program import fib_recursive, matrix_multiply, sieve_of_eratosthenes  # noqa: E402


def main() -> None:
    """Смешанная нагрузка: чистый Python, NumPy и работа с памятью."""
    for _ in range(3):
        fib_recursive(23)
        matrix_multiply(150)
        sieve_of_eratosthenes(100000)


if __name__ == "__main__":
    main()
