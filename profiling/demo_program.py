"""Демо-программа для исследования инструментов профилирования.

Пять функций четырёх классов сложности плюс функция нагрузки на память:
    fib_recursive         — рекурсивный Фибоначчи, O(2^n);
    fib_iterative         — итеративный Фибоначчи, O(n);
    matrix_multiply       — умножение матриц через NumPy, O(n^3);
    sieve_of_eratosthenes — решето Эратосфена, O(n log log n);
    memory_churn          — интенсивное выделение и освобождение памяти.
"""

import numpy as np


def fib_recursive(n):
    """Рекурсивный Фибоначчи, O(2^n)."""
    return n if n < 2 else fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    """Итеративный Фибоначчи, O(n)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def matrix_multiply(n):
    """Умножение квадратных матриц n x n через NumPy, O(n^3)."""
    return np.random.rand(n, n) @ np.random.rand(n, n)


def sieve_of_eratosthenes(n):
    """Решето Эратосфена: все простые числа до n, O(n log log n)."""
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    return [i for i, v in enumerate(s) if v]


def memory_churn():
    """Нагрузка на память: 100 списков по 1000 элементов за вызов."""
    return len([list(range(1000)) for _ in range(100)])
