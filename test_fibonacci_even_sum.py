"""Автоматические тесты fibonacci_even_sum.py: ровно 5 тестов на каждую ГЛАВНУЮ функцию.

Учебная практика ПМ.06, вариант 1.
Главные функции: even_fibonacci_sum, parse_limit, format_result,
read_limit_from_console, read_limit_from_file, main (CLI).
Графический интерфейс (run_gui) проверяется вручную по тест-кейсам.

Запуск (из папки проекта):
    python test_fibonacci_even_sum.py
    python -m unittest -v
"""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))  # если тесты лежат в подпапке tests/
import fibonacci_even_sum as prog  # noqa: E402


# --------------------------------------------------------------------------- помощники
def reference_sum(limit):
    """Независимая эталонная реализация: ряд 0, 1, 1, 2, 3, 5, ..."""
    total, a, b = 0, 0, 1
    while a <= limit:
        if a % 2 == 0:
            total += a
        a, b = b, a + b
    return total


def run_main(argv, inputs=()):
    """Запускает prog.main, возвращает (код, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        with mock.patch.object(sys, "argv", ["fibonacci_even_sum.py", *argv]):
            with mock.patch("builtins.input", side_effect=list(inputs) + [EOFError()] * 50):
                code = prog.main()
    return code, out.getvalue(), err.getvalue()


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.src = self.base / "input.txt"
        self.dst = self.base / "result.txt"

    def write_input(self, text):
        self.src.write_text(text, encoding="utf-8")
        return self.src


# =========================================================================== расчёт
class EvenFibonacciSumTests(unittest.TestCase):
    def test_typical_limits(self):
        for limit, expected in ((10, 10), (100, 44), (1000, 798), (4_000_000, 4_613_732)):
            self.assertEqual(prog.even_fibonacci_sum(limit), expected, msg=limit)

    def test_boundary_values_limit_is_included(self):
        for limit, expected in ((0, 0), (1, 0), (2, 2), (7, 2), (8, 10), (33, 10), (34, 44)):
            self.assertEqual(prog.even_fibonacci_sum(limit), expected, msg=limit)

    def test_negative_limit_rejected(self):
        for bad in (-1, -10, -10 ** 30):
            with self.assertRaises(ValueError, msg=bad) as ctx:
                prog.even_fibonacci_sum(bad)
            self.assertIn("неотрицательным", str(ctx.exception))

    def test_matches_reference_for_range(self):
        for limit in range(0, 2001):
            self.assertEqual(prog.even_fibonacci_sum(limit), reference_sum(limit), msg=limit)

    def test_huge_limit_and_result_type(self):
        limit = 10 ** 30
        result = prog.even_fibonacci_sum(limit)
        self.assertIsInstance(result, int)
        self.assertEqual(result, reference_sum(limit))
        self.assertEqual(result % 2, 0)  # сумма чётных чисел чётна


# =========================================================================== разбор ввода
class ParseLimitTests(unittest.TestCase):
    def test_plain_numbers_and_spaces(self):
        self.assertEqual(prog.parse_limit("100"), 100)
        self.assertEqual(prog.parse_limit("  42  "), 42)
        self.assertEqual(prog.parse_limit("0"), 0)
        self.assertEqual(prog.parse_limit("\t7\n"), 7)

    def test_empty_and_blank_rejected(self):
        for bad in ("", "   ", "\n", "\t"):
            with self.assertRaises(ValueError, msg=repr(bad)) as ctx:
                prog.parse_limit(bad)
            self.assertIn("Введите предельное значение", str(ctx.exception))

    def test_non_integer_rejected(self):
        for bad in ("abc", "12.5", "1,5", "1 2", "1e3", "10 x", "--5"):
            with self.assertRaises(ValueError, msg=bad) as ctx:
                prog.parse_limit(bad)
            self.assertIn("целое число", str(ctx.exception))

    def test_error_has_no_chained_traceback(self):
        with self.assertRaises(ValueError) as ctx:
            prog.parse_limit("abc")
        self.assertIsNone(ctx.exception.__cause__)
        self.assertTrue(ctx.exception.__suppress_context__)

    def test_signs_leading_zeros_and_huge(self):
        self.assertEqual(prog.parse_limit("+7"), 7)
        self.assertEqual(prog.parse_limit("007"), 7)
        self.assertEqual(prog.parse_limit("-5"), -5)  # знак проверяет расчёт, а не разбор
        self.assertEqual(prog.parse_limit("1" + "0" * 30), 10 ** 30)


# =========================================================================== форматирование
class FormatResultTests(unittest.TestCase):
    def test_exact_text(self):
        self.assertEqual(prog.format_result(100, 44), "Сумма чётных чисел Фибоначчи до 100: 44")

    def test_zero_values(self):
        self.assertEqual(prog.format_result(0, 0), "Сумма чётных чисел Фибоначчи до 0: 0")

    def test_huge_numbers(self):
        text = prog.format_result(10 ** 30, 12345)
        self.assertEqual(text, "Сумма чётных чисел Фибоначчи до {}: 12345".format(10 ** 30))

    def test_no_trailing_newline_and_is_str(self):
        text = prog.format_result(10, 10)
        self.assertIsInstance(text, str)
        self.assertFalse(text.endswith("\n"))

    def test_limit_before_colon_and_result_after(self):
        left, right = prog.format_result(1000, 798).split(": ")
        self.assertTrue(left.endswith("1000"))
        self.assertEqual(right, "798")


# =========================================================================== ввод из консоли
class ReadLimitFromConsoleTests(unittest.TestCase):
    def read(self, inputs):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            with mock.patch("builtins.input", side_effect=inputs) as fake:
                value = prog.read_limit_from_console()
        return value, out.getvalue(), fake

    def test_valid_number(self):
        value, out, _ = self.read(["100"])
        self.assertEqual(value, 100)
        self.assertEqual(out, "")

    def test_spaces_stripped(self):
        self.assertEqual(self.read(["  42  "])[0], 42)

    def test_bad_then_good_asks_again(self):
        value, out, fake = self.read(["abc", "10"])
        self.assertEqual(value, 10)
        self.assertEqual(fake.call_count, 2)
        self.assertIn("Ошибка: введите целое число.", out)

    def test_several_bad_inputs_each_reported(self):
        value, out, _ = self.read(["abc", "", "12.5", "8"])
        self.assertEqual(value, 8)
        self.assertEqual(out.count("Ошибка: введите целое число."), 3)

    def test_prompt_text_and_negative_accepted(self):
        value, _, fake = self.read(["-5"])
        self.assertEqual(value, -5)  # отрицательное значение отклоняет расчёт, а не ввод
        fake.assert_called_with("Введите предельное значение: ")


# =========================================================================== ввод из файла
class ReadLimitFromFileTests(TempDirCase):
    def test_reads_number_with_newline(self):
        self.assertEqual(prog.read_limit_from_file(str(self.write_input("100\n"))), 100)

    def test_spaces_and_crlf_stripped(self):
        self.assertEqual(prog.read_limit_from_file(str(self.write_input("  \r\n 55 \r\n"))), 55)

    def test_missing_file_raises_oserror(self):
        with self.assertRaises(OSError):
            prog.read_limit_from_file(str(self.base / "no_such_file.txt"))

    def test_invalid_content_raises_valueerror(self):
        for content in ("abc", "", "   ", "12.5", "1 2"):
            self.write_input(content)
            with self.assertRaises(ValueError, msg=repr(content)):
                prog.read_limit_from_file(str(self.src))

    def test_folder_instead_of_file_and_negative_value(self):
        with self.assertRaises(OSError):
            prog.read_limit_from_file(str(self.base))
        self.assertEqual(prog.read_limit_from_file(str(self.write_input("-5"))), -5)


# =========================================================================== CLI
class MainTests(TempDirCase):
    def test_console_mode_returns_0_and_prints_result(self):
        code, out, err = run_main(["--console"], inputs=["10"])
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, "Сумма чётных чисел Фибоначчи до 10: 10\n")

    def test_file_input_and_output(self):
        self.write_input("100\n")
        code, out, err = run_main(["--input", str(self.src), "--output", str(self.dst)])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Результат записан", out)
        self.assertEqual(self.dst.read_text(encoding="utf-8"),
                         "Сумма чётных чисел Фибоначчи до 100: 44\n")

    def test_file_input_prints_to_stdout_without_output_file(self):
        self.write_input("1000")
        code, out, _ = run_main(["--input", str(self.src)])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Сумма чётных чисел Фибоначчи до 1000: 798\n")
        self.assertFalse(self.dst.exists())

    def test_errors_return_1_without_traceback(self):
        for content in ("abc", "", "12.5", "-5"):
            self.write_input(content)
            code, out, err = run_main(["--input", str(self.src)])
            self.assertEqual(code, 1, msg=repr(content))
            self.assertIn("Ошибка", err, msg=repr(content))
            self.assertNotIn("Traceback", err + out, msg=repr(content))
        code, _, err = run_main(["--input", str(self.base / "no_such_file.txt")])
        self.assertEqual(code, 1)
        self.assertIn("Ошибка", err)
        self.assertFalse(self.dst.exists())

    def test_no_arguments_starts_gui_and_handles_missing_tkinter(self):
        with mock.patch.object(prog, "run_gui") as gui:
            code, _, _ = run_main([])
        self.assertEqual(code, 0)
        gui.assert_called_once()
        with mock.patch.object(prog, "run_gui", side_effect=ImportError("no tkinter")):
            code, _, err = run_main([])
        self.assertEqual(code, 1)
        self.assertIn("--console", err)


class SummaryResult(unittest.TextTestResult):
    """Считает успешные тесты и ведёт счёт по классам (функциям)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.per_class = {}

    def _count(self, test, ok):
        name = type(test).__name__
        done, total = self.per_class.get(name, (0, 0))
        self.per_class[name] = (done + (1 if ok else 0), total + 1)

    def addSuccess(self, test):
        super().addSuccess(test)
        self._count(test, True)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._count(test, False)

    def addError(self, test, err):
        super().addError(test, err)
        self._count(test, False)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._count(test, False)


class SummaryRunner(unittest.TextTestRunner):
    """Запуск с итогом: сколько тестов прошло успешно (всего и по каждой функции)."""
    resultclass = SummaryResult

    def run(self, test):
        result = super().run(test)
        out = self.stream
        out.writeln("")
        out.writeln("ИТОГИ ПО ФУНКЦИЯМ (успешно / всего):")
        for name, (done, total) in sorted(result.per_class.items()):
            mark = "OK    " if done == total else "ОШИБКА"
            out.writeln("  {} {:<28} {}/{}".format(mark, name.replace("Tests", ""), done, total))
        passed = sum(done for done, _ in result.per_class.values())
        out.writeln("")
        out.writeln("УСПЕШНО ПРОЙДЕНО ТЕСТОВ: {} из {}".format(passed, result.testsRun))
        out.writeln("Провалено: {}, ошибок: {}, пропущено: {}".format(
            len(result.failures), len(result.errors), len(result.skipped)))
        return result


if __name__ == "__main__":
    unittest.main(testRunner=SummaryRunner, verbosity=1)
