"""Целевой процесс для py-spy: непрерывная смешанная нагрузка.

py-spy подключается к уже запущенному процессу без изменения кода:
    py-spy record -o profiling/flame.svg --duration 5 -- python profiling/spin.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_program import fib_iterative, fib_recursive, sieve_of_eratosthenes  # noqa: E402


def main() -> None:
    """Цикл нагрузки примерно на 8 секунд."""
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        fib_recursive(24)
        fib_iterative(20000)
        sieve_of_eratosthenes(200000)


if __name__ == "__main__":
    main()
