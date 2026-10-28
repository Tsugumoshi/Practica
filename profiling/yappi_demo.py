"""Многопоточное профилирование (yappi).

Yappi корректно различает потоки, в отличие от cProfile.
Запуск из каталога репозитория:
    python profiling/yappi_demo.py
"""

import sys
import threading
from pathlib import Path

import yappi

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_program import fib_iterative, fib_recursive  # noqa: E402

_WORKER_RESULT = {}


def worker(name: str, value: int) -> None:
    """Рабочая функция потока: тяжёлая рекурсия + лёгкая итерация."""
    _WORKER_RESULT[name] = (fib_recursive(value), fib_iterative(2000))


def main() -> None:
    """Три потока с разной нагрузкой; замер по CPU-времени."""
    yappi.set_clock_type("cpu")
    yappi.start()
    threads = [
        threading.Thread(target=worker, args=(f"t{i}", 10 + i)) for i in range(3)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    yappi.stop()

    print("=" * 70)
    print("5. YAPPI — CPU-время, три потока (fib_recursive(10..12))")
    print("=" * 70)
    yappi.get_func_stats().sort("ttot").print_all(columns={
        0: ("name", 48),
        1: ("ncall", 10),
        2: ("ttot", 10),
        3: ("tsub", 10),
    })

    print("=" * 70)
    print("Потоки:")
    print("=" * 70)
    yappi.get_thread_stats().print_all()


if __name__ == "__main__":
    main()
