"""Сумма чётных чисел Фибоначчи, не превышающих заданное значение.

Учебная практика ПМ.06 «Сопровождение информационных систем», вариант 1.

Программа принимает целое неотрицательное значение из консоли или из
файла (--input ПУТЬ) и выводит сумму всех чётных элементов ряда
Фибоначчи, не превышающих это значение, на экран и (необязательно)
в файл (--output ПУТЬ).

Используется только стандартная библиотека Python 3.10+.
"""

import argparse
import re
import sys
from pathlib import Path

# Строгая проверка: строка должна состоять только из цифр
# (допускается необязательный знак «+» или «-»).
_INTEGER_RE = re.compile(r"^[+-]?\d+$")


def even_fibonacci_sum(limit: int) -> int:
    """Сумма чётных чисел Фибоначчи, не превышающих limit.

    Ряд: 1, 2, 3, 5, 8, ... Элемент, равный limit, учитывается.
    Для limit < 0 выбрасывается ValueError.
    """
    if limit < 0:
        raise ValueError("Значение должно быть неотрицательным")
    a, b = 1, 2
    total = 0
    while a <= limit:
        if a % 2 == 0:
            total += a
        a, b = b, a + b
    return total


def parse_limit(raw: str) -> int:
    """Разобрать строку и вернуть целое неотрицательное число.

    Бросает ValueError с понятным сообщением, если строка пустая,
    не является целым числом или число отрицательное.
    """
    text = raw.strip()
    if not text:
        raise ValueError("введена пустая строка")
    if not _INTEGER_RE.fullmatch(text):
        raise ValueError("введите целое число")
    value = int(text)
    if value < 0:
        raise ValueError("Значение должно быть неотрицательным")
    return value


def read_limit_from_console() -> int:
    """Запросить значение из консоли и повторять запрос при ошибке.

    EOFError (Ctrl+D / Ctrl+Z) не перехватывается здесь — его
    обрабатывает main().
    """
    while True:
        raw = input("Введите целое неотрицательное число: ")
        try:
            return parse_limit(raw)
        except ValueError as exc:
            print(f"Ошибка: {exc}. Попробуйте ещё раз.")


def read_limit_from_file(path: str) -> int:
    """Прочитать значение из файла в кодировке UTF-8 (допускается BOM).

    Бросает ValueError с сообщением, указывающим файл, если файл не
    читается или не содержит одного целого неотрицательного числа.
    """
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
    except OSError as exc:
        reason = exc.strerror or str(exc)
        raise ValueError(f"не удалось прочитать файл «{path}»: {reason}") from exc
    try:
        return parse_limit(text)
    except ValueError as exc:
        raise ValueError(
            f"в файле «{path}» должно быть одно целое число ({exc})"
        ) from exc


def build_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="fibonacci_even_sum",
        description=(
            "Вычисление суммы всех чётных элементов ряда Фибоначчи, "
            "не превышающих заданное значение."
        ),
    )
    parser.add_argument(
        "--input",
        metavar="ПУТЬ",
        help="читать значение из файла вместо консоли",
    )
    parser.add_argument(
        "--output",
        metavar="ПУТЬ",
        help="дополнительно записать результат в файл",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Точка входа: ввод, вычисление, вывод. Возвращает код завершения.

    Коды: 0 — успех; 1 — ошибка ввода/вывода (программа не завершается
    аварийно ни при каком некорректном вводе).
    """
    args = build_parser().parse_args(argv)

    try:
        if args.input:
            limit = read_limit_from_file(args.input)
        else:
            limit = read_limit_from_console()
    except (EOFError, KeyboardInterrupt):
        print()
        print("Ввод прерван пользователем.")
        return 1
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return 1

    result = even_fibonacci_sum(limit)
    line = f"Сумма чётных чисел Фибоначчи до {limit}: {result}"
    print(line)

    if args.output:
        try:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(line + "\n", encoding="utf-8")
            print(f"Результат записан в файл: {args.output}")
        except OSError as exc:
            reason = exc.strerror or str(exc)
            print(f"Ошибка записи в файл «{args.output}»: {reason}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
