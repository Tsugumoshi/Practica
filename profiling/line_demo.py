"""Построчный профилировщик времени (line_profiler).

Декоратор применяется к импортированным функциям, чтобы получить
построчную картину внутри самих функций demo_program.py.

Запуск из каталога репозитория:
    kernprof -l -v profiling/line_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_program import fib_recursive, sieve_of_eratosthenes  # noqa: E402

# kernprof внедряет @profile в builtins при запуске через kernprof -l
fib_recursive_p = profile(fib_recursive)  # noqa: F821
sieve_p = profile(sieve_of_eratosthenes)  # noqa: F821


def main():
    """Две функции: экспоненциальная рекурсия и линейные циклы."""
    fib_recursive_p(20)
    sieve_p(100000)


if __name__ == "__main__":
    main()
