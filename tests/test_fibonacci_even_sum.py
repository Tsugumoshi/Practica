"""Автоматические тесты основной программы fibonacci_even_sum.py.

Каждый тест соответствует тест-кейсу из docs/Тест-кейсы.md; идентификатор
кейса указан в строке документации теста (например, TC-F-01).
Запуск: python -m unittest discover -v
"""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import fibonacci_even_sum as fib  # noqa: E402


class EvenFibonacciSumTests(unittest.TestCase):
    """Тест-кейсы функции even_fibonacci_sum(limit)."""

    def test_zero_limit_returns_zero(self):
        """TC-F-01: предел 0 — сумма равна 0."""
        self.assertEqual(fib.even_fibonacci_sum(0), 0)

    def test_limit_ten_returns_ten(self):
        """TC-F-02: предел 10 — учитываются 2 и 8, сумма 10."""
        self.assertEqual(fib.even_fibonacci_sum(10), 10)

    def test_limit_hundred_returns_forty_four(self):
        """TC-F-03: предел 100 — учитываются 2, 8, 34, сумма 44."""
        self.assertEqual(fib.even_fibonacci_sum(100), 44)

    def test_projector_limit_four_million(self):
        """TC-F-04: предел 4 000 000 — эталонный результат 4 613 732."""
        self.assertEqual(fib.even_fibonacci_sum(4_000_000), 4_613_732)

    def test_negative_limit_raises(self):
        """TC-F-05: предел -5 — ValueError без аварийного завершения."""
        with self.assertRaises(ValueError):
            fib.even_fibonacci_sum(-5)


class ParseLimitTests(unittest.TestCase):
    """Тест-кейсы функции parse_limit(raw)."""

    def test_valid_integer(self):
        """TC-P-01: строка «42» — возвращается 42."""
        self.assertEqual(fib.parse_limit("42"), 42)

    def test_strict_parsing_rejects_underscores(self):
        """TC-P-02: строка «1_000» — ValueError (нестрогий разбор запрещён)."""
        with self.assertRaises(ValueError):
            fib.parse_limit("1_000")

    def test_non_numeric_rejected(self):
        """TC-P-03: строка «abc» — ValueError с понятным сообщением."""
        with self.assertRaises(ValueError):
            fib.parse_limit("abc")

    def test_empty_string_rejected(self):
        """TC-P-04: пустая строка — ValueError."""
        with self.assertRaises(ValueError):
            fib.parse_limit("   ")

    def test_negative_rejected(self):
        """TC-P-05: строка «-3» — ValueError."""
        with self.assertRaises(ValueError):
            fib.parse_limit("-3")


class ReadLimitFromConsoleTests(unittest.TestCase):
    """Тест-кейсы функции read_limit_from_console()."""

    def test_single_valid_input(self):
        """TC-C-01: ввод «10» — возвращается 10."""
        with mock.patch("builtins.input", return_value="10"):
            self.assertEqual(fib.read_limit_from_console(), 10)

    def test_repeat_after_non_numeric(self):
        """TC-C-02: ввод «abc», затем «8» — запрос повторяется, ответ 8."""
        with mock.patch("builtins.input", side_effect=["abc", "8"]):
            with redirect_stdout(io.StringIO()) as out:
                self.assertEqual(fib.read_limit_from_console(), 8)
        self.assertIn("введите целое число", out.getvalue())

    def test_repeat_after_empty(self):
        """TC-C-03: пустой ввод, затем «5» — запрос повторяется, ответ 5."""
        with mock.patch("builtins.input", side_effect=["", "5"]):
            self.assertEqual(fib.read_limit_from_console(), 5)

    def test_repeat_after_negative(self):
        """TC-C-04: ввод «-7», затем «3» — запрос повторяется, ответ 3."""
        with mock.patch("builtins.input", side_effect=["-7", "3"]):
            self.assertEqual(fib.read_limit_from_console(), 3)

    def test_eof_error_propagates(self):
        """TC-C-05: закрытый ввод (Ctrl+D) — EOFError обрабатывается в main()."""
        with mock.patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(EOFError):
                fib.read_limit_from_console()


class ReadLimitFromFileTests(unittest.TestCase):
    """Тест-кейсы функции read_limit_from_file(path)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, name: str, text: str) -> str:
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_valid_file(self):
        """TC-R-01: файл со строкой «25» — возвращается 25."""
        self.assertEqual(fib.read_limit_from_file(self._write("ok.txt", "25")), 25)

    def test_file_with_bom(self):
        """TC-R-02: файл с BOM (Блокнот Windows) — значение 15 читается."""
        path = self.dir / "bom.txt"
        path.write_bytes("15".encode("utf-8-sig"))
        self.assertEqual(fib.read_limit_from_file(str(path)), 15)

    def test_text_file_rejected(self):
        """TC-R-03: файл с текстом «abc» — ValueError с именем файла."""
        path = self._write("bad.txt", "abc")
        with self.assertRaises(ValueError) as ctx:
            fib.read_limit_from_file(path)
        self.assertIn("bad.txt", str(ctx.exception))

    def test_empty_file_rejected(self):
        """TC-R-04: пустой файл — ValueError с именем файла."""
        path = self._write("empty.txt", "")
        with self.assertRaises(ValueError):
            fib.read_limit_from_file(path)

    def test_missing_file_rejected(self):
        """TC-R-05: отсутствующий файл — ValueError без трассировки."""
        with self.assertRaises(ValueError):
            fib.read_limit_from_file(str(self.dir / "no_such_file.txt"))


class MainTests(unittest.TestCase):
    """Тест-кейсы функции main(argv)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, argv):
        with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()):
            code = fib.main(argv)
        return code, out.getvalue()

    def test_input_file_and_output_file(self):
        """TC-M-01: --input и --output — код 0, результат в обоих каналах."""
        src = self.dir / "in.txt"
        src.write_text("10", encoding="utf-8")
        dst = self.dir / "out" / "result.txt"
        code, out = self._run(["--input", str(src), "--output", str(dst)])
        self.assertEqual(code, 0)
        self.assertIn("Сумма чётных чисел Фибоначчи до 10: 10", out)
        self.assertIn(
            "Сумма чётных чисел Фибоначчи до 10: 10", dst.read_text(encoding="utf-8")
        )

    def test_console_mode(self):
        """TC-M-02: без аргументов ввод из консоли «100» — код 0, ответ 44."""
        with mock.patch("builtins.input", return_value="100"):
            code, out = self._run([])
        self.assertEqual(code, 0)
        self.assertIn("Сумма чётных чисел Фибоначчи до 100: 44", out)

    def test_missing_input_file(self):
        """TC-M-03: --input на отсутствующий файл — код 1, сообщение об ошибке."""
        code, out = self._run(["--input", str(self.dir / "ghost.txt")])
        self.assertEqual(code, 1)
        self.assertIn("Ошибка", out)

    def test_output_write_error(self):
        """TC-M-04: --output в несуществующий корень — код 1 без трассировки."""
        src = self.dir / "in.txt"
        src.write_text("10", encoding="utf-8")
        code, out = self._run(
            ["--input", str(src), "--output", "/nonexistent_dir_xyz/r.txt"]
        )
        self.assertEqual(code, 1)
        self.assertIn("Ошибка записи", out)

    def test_console_eof_handled(self):
        """TC-M-05: закрытый консольный ввод — код 1, без трассировки."""
        with mock.patch("builtins.input", side_effect=EOFError):
            code, out = self._run([])
        self.assertEqual(code, 1)
        self.assertIn("Ввод прерван", out)

    def test_bad_file_content_exit_code(self):
        """TC-M-06: --input файл с «abc» — код 1, сообщение с именем файла."""
        src = self.dir / "bad.txt"
        src.write_text("abc", encoding="utf-8")
        code, out = self._run(["--input", str(src)])
        self.assertEqual(code, 1)
        self.assertIn("bad.txt", out)


if __name__ == "__main__":
    unittest.main()
