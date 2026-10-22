#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Учебная практика ПМ.06. Вариант 1.
Сумма всех чётных элементов ряда Фибоначчи,
не превышающих заданное пользователем значение.

Автор: Абрамов Илья Сергеевич, гр. ИСП-31с
"""

import argparse
import sys


def even_fibonacci_sum(limit: int) -> int:
    """Возвращает сумму чётных чисел Фибоначчи, не превышающих limit."""
    if limit < 0:
        raise ValueError("Значение должно быть неотрицательным")
    a, b = 1, 2
    total = 0
    while a <= limit:
        if a % 2 == 0:
            total += a
        a, b = b, a + b
    return total


def read_limit_from_console() -> int:
    while True:
        try:
            raw = input("Введите предельное значение: ").strip()
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")


def read_limit_from_file(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        return int(f.read().strip())


def main() -> int:
    parser = argparse.ArgumentParser(description="Сумма чётных чисел Фибоначчи")
    parser.add_argument("--input", help="Файл с предельным значением")
    parser.add_argument("--output", help="Файл для записи результата")
    args = parser.parse_args()

    try:
        limit = read_limit_from_file(args.input) if args.input else read_limit_from_console()
        result = even_fibonacci_sum(limit)
    except (ValueError, OSError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1

    text = f"Сумма чётных чисел Фибоначчи до {limit}: {result}"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Результат записан в {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
