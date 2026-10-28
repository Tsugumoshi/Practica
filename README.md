[![CI](https://github.com/Tsugumoshi/Practica/actions/workflows/tests.yml/badge.svg)](https://github.com/Tsugumoshi/Practica/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-51%20passed-brightgreen)](#запуск-тестов)

# Сумма чётных чисел Фибоначчи

Учебный проект по практике ПМ.06 **«Сопровождение информационных систем»**
(специальность 09.02.07, группа ИСП-31с, период 19.10.2026–31.10.2026, 72 часа).

**Вариант 1:** консольная программа на Python для нахождения суммы всех чётных
элементов ряда Фибоначчи, которые не превышают указанное пользователем значение,
с вводом и выводом данных через консоль и через файл. Дополнительно разработан
модуль резервного копирования и восстановления данных с проверкой целостности
по SHA-256.

- **Исполнитель:** Абрамов И.С.
- **Руководитель практики:** Шашкова В.Д.
- **Языки:** Русский | [English](#english)

---

## Возможности

- ввод значения из **консоли** (с повтором запроса при ошибке) или из **файла** (`--input`);
- вывод результата на **экран** и дополнительно в **файл** (`--output`);
- строгая проверка ввода: целое неотрицательное число (строка «1_000» не принимается);
- обработка всех ошибок без аварийного завершения: файлы с BOM, отсутствующие
  файлы, закрытый ввод (Ctrl+D/Ctrl+Z), недоступный каталог записи;
- резервное копирование в ZIP с манифестом SHA-256, проверка целостности и
  безопасное восстановление;
- 51 автоматический тест (unittest) и CI на GitHub Actions;
- сценарии профилирования встроенными средствами Python: timeit, cProfile,
  tracemalloc.

## Структура проекта

```text
Practica/
├── README.md                      # руководство пользователя (RU + EN)
├── .github/workflows/tests.yml    # CI: тесты + black --check
├── src/
│   ├── fibonacci_even_sum.py      # основная программа
│   └── backup_restore.py          # резервное копирование и восстановление
├── tests/
│   ├── test_fibonacci_even_sum.py # тесты основной программы
│   └── test_backup_restore.py     # тесты модуля копирования
├── docs/
│   ├── ТЗ.md                      # техническое задание (ГОСТ 19.201-78)
│   ├── Регламент_ТО.md            # регламент технического обслуживания
│   └── Тест-кейсы.md              # 51 тест-кейс
├── profiling/
│   ├── demo_program.py            # демо-программа для профилирования
│   ├── run_benchmarks.py          # timeit + cProfile + tracemalloc
│   └── Результаты_профилирования.md
└── examples/
    └── input.txt                  # пример входного файла
```

## Функции

| Функция | Модуль | Назначение |
|---|---|---|
| `even_fibonacci_sum(limit)` | fibonacci_even_sum | Сумма чётных чисел Фибоначчи, не превышающих limit |
| `parse_limit(raw)` | fibonacci_even_sum | Разбор и проверка введённой строки |
| `read_limit_from_console()` | fibonacci_even_sum | Ввод из консоли с повтором запроса при ошибке |
| `read_limit_from_file(path)` | fibonacci_even_sum | Чтение значения из файла (UTF-8, допускается BOM) |
| `main(argv)` | fibonacci_even_sum | Аргументы командной строки, ввод, вывод, коды завершения |
| `sha256_file(path)` | backup_restore | Контрольная сумма SHA-256 файла |
| `create_backup(source_dir, backup_dir)` | backup_restore | Полная копия проекта в ZIP с манифестом |
| `verify_backup(zip_path)` | backup_restore | Проверка целостности копии |
| `restore_backup(zip_path, dest_dir)` | backup_restore | Восстановление из проверенной копии |
| `main(argv)` | backup_restore | Команды backup, verify, restore |

## Системные требования

- Python **3.10+** (проверялось на Python 3.12);
- ОС: Windows, Linux или macOS;
- сторонние зависимости **не требуются** — используется только стандартная
  библиотека. Для профилирования по желанию: `pip install -r requirements-dev.txt`.

## Установка

```bash
git clone https://github.com/Tsugumoshi/Practica.git
cd Practica
```

## Запуск программы

Все четыре режима:

```bash
# 1. Ввод из консоли, вывод на экран
python src/fibonacci_even_sum.py

# 2. Ввод из файла, вывод на экран
python src/fibonacci_even_sum.py --input examples/input.txt

# 3. Ввод из консоли, результат дополнительно в файл
python src/fibonacci_even_sum.py --output result.txt

# 4. Ввод из файла и вывод в файл
python src/fibonacci_even_sum.py --input examples/input.txt --output result.txt
```

Примеры работы:

| Ввод | Результат |
|---|---|
| `10` | Сумма чётных чисел Фибоначчи до 10: 10 |
| `100` | Сумма чётных чисел Фибоначчи до 100: 44 |
| `4000000` | Сумма чётных чисел Фибоначчи до 4000000: 4613732 |
| `0` | Сумма чётных чисел Фибоначчи до 0: 0 |
| `-5` | Ошибка: Значение должно быть неотрицательным (код 1) |

## Резервное копирование и восстановление

```bash
python src/backup_restore.py backup . backups      # создать копию
python src/backup_restore.py verify backups/ИМЯ.zip # проверить целостность
python src/backup_restore.py restore backups/ИМЯ.zip папка  # восстановить
```

Схема — полное копирование с меткой времени в имени архива
(`backup_ГГГГММДД_ЧЧММСС.zip`) и манифестом `manifest.sha256` внутри архива.
Восстановление выполняется только после успешной проверки; выход за пределы
каталога назначения запрещён.

## Запуск тестов

```bash
python -m unittest discover -v   # 51 тест
black --check src tests          # проверка код-стайла
```

## Профилирование

```bash
python profiling/run_benchmarks.py   # timeit + cProfile + tracemalloc одним запуском
```

Отдельные инструменты встроены в Python и запускаются напрямую:

```bash
python -m cProfile -s tottime profiling/demo_program.py   # время по функциям
python -m timeit -n 10 -r 5 "..."                          # микро-замер выражения
```

Полные результаты и выводы — в
[profiling/Результаты_профилирования.md](profiling/Результаты_профилирования.md).

## Частые ошибки и способы их устранения

| Сообщение | Причина | Решение |
|---|---|---|
| «введите целое число» | Введён текст вместо числа | Ввести целое число, например `100` |
| «Значение должно быть неотрицательным» | Введено отрицательное значение | Ввести число ≥ 0 |
| «в файле … должно быть одно целое число» | Файл содержит текст или пуст | Подготовить файл с одним целым числом |
| «не удалось прочитать файл …» | Файл не существует или недоступен | Проверить путь и права доступа |
| «Ошибка записи в файл …» | Каталог назначения недоступен | Проверить путь и права записи |
| «Ввод прерван пользователем.» | Нажат Ctrl+D / Ctrl+Z | Повторить запуск |
| «Копия повреждена или отсутствует!» | Архив изменён после создания | Использовать другой архив или создать новый |

## Документация

- [docs/ТЗ.md](docs/ТЗ.md) — техническое задание;
- [docs/Регламент_ТО.md](docs/Регламент_ТО.md) — регламент технического обслуживания;
- [docs/Тест-кейсы.md](docs/Тест-кейсы.md) — тест-кейсы.

---

<a name="english"></a>

[![CI](https://github.com/Tsugumoshi/Practica/actions/workflows/tests.yml/badge.svg)](https://github.com/Tsugumoshi/Practica/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-51%20passed-brightgreen)](#running-the-tests)

# Sum of Even Fibonacci Numbers

An educational project for the internship module PM.06 **"Information Systems
Maintenance"** (specialty 09.02.07, group ISP-31s, 19 Oct 2026 – 31 Oct 2026,
72 hours).

**Variant 1:** a Python console program that computes the sum of all even
Fibonacci numbers not exceeding a user-defined limit, with input and output
via console and file. Additionally, a backup and restore module with SHA-256
integrity checks was developed.

- **Author:** Abramov I.S.
- **Internship supervisor:** Shashkova V.D.
- **Languages:** [Русский](#) | English

## Features

- input from the **console** (re-asks on invalid input) or from a **file** (`--input`);
- output to the **screen** and optionally to a **file** (`--output`);
- strict input validation: a non-negative integer (strings like `1_000` are rejected);
- graceful error handling: BOM files, missing files, closed input
  (Ctrl+D/Ctrl+Z), unwritable output paths — no tracebacks, exit code 1;
- ZIP backups with a SHA-256 manifest, integrity verification, safe restore;
- 51 automated tests (unittest) and GitHub Actions CI;
- profiling scripts: timeit, cProfile, tracemalloc (Python standard library).

## Project structure

```text
Practica/
├── README.md                      # user guide (RU + EN)
├── .github/workflows/tests.yml    # CI: tests + black --check
├── src/
│   ├── fibonacci_even_sum.py      # main program
│   └── backup_restore.py          # backup and restore
├── tests/                         # automated tests
├── docs/
│   ├── ТЗ.md                      # technical specification (GOST 19.201-78)
│   ├── Регламент_ТО.md            # maintenance regulations
│   └── Тест-кейсы.md              # 51 test cases
├── profiling/                     # profiling scripts and results
└── examples/
    └── input.txt                  # sample input file
```

## Functions

| Function | Module | Purpose |
|---|---|---|
| `even_fibonacci_sum(limit)` | fibonacci_even_sum | Sum of even Fibonacci numbers ≤ limit |
| `parse_limit(raw)` | fibonacci_even_sum | Parse and validate the input string |
| `read_limit_from_console()` | fibonacci_even_sum | Console input with re-ask on error |
| `read_limit_from_file(path)` | fibonacci_even_sum | Read value from file (UTF-8, BOM allowed) |
| `main(argv)` | fibonacci_even_sum | CLI arguments, input, output, exit codes |
| `sha256_file(path)` | backup_restore | SHA-256 checksum of a file |
| `create_backup(source_dir, backup_dir)` | backup_restore | Full project backup into a ZIP with a manifest |
| `verify_backup(zip_path)` | backup_restore | Verify backup integrity |
| `restore_backup(zip_path, dest_dir)` | backup_restore | Restore from a verified backup |
| `main(argv)` | backup_restore | Commands: backup, verify, restore |

## Requirements

- Python **3.10+** (tested on Python 3.12);
- OS: Windows, Linux or macOS;
- **no third-party dependencies** — standard library only.
  Optional profiling tools: `pip install -r requirements-dev.txt`.

## Installation

```bash
git clone https://github.com/Tsugumoshi/Practica.git
cd Practica
```

## Usage

All four modes:

```bash
# 1. Console input, screen output
python src/fibonacci_even_sum.py

# 2. File input, screen output
python src/fibonacci_even_sum.py --input examples/input.txt

# 3. Console input, result additionally written to a file
python src/fibonacci_even_sum.py --output result.txt

# 4. File input and file output
python src/fibonacci_even_sum.py --input examples/input.txt --output result.txt
```

Examples:

| Input | Output |
|---|---|
| `10` | Сумма чётных чисел Фибоначчи до 10: 10 |
| `100` | Сумма чётных чисел Фибоначчи до 100: 44 |
| `4000000` | Сумма чётных чисел Фибоначчи до 4000000: 4613732 |
| `0` | Сумма чётных чисел Фибоначчи до 0: 0 |
| `-5` | Error: the value must be non-negative (exit code 1) |

> Program messages are displayed in Russian per the technical specification.

## Backup and restore

```bash
python src/backup_restore.py backup . backups        # create a backup
python src/backup_restore.py verify backups/NAME.zip  # verify integrity
python src/backup_restore.py restore backups/NAME.zip folder  # restore
```

The scheme is a full copy with a timestamp in the archive name
(`backup_YYYYMMDD_HHMMSS.zip`) and a `manifest.sha256` manifest inside.
Restoration runs only after a successful integrity check; extracting files
outside the destination directory is forbidden.

## Running the tests

```bash
python -m unittest discover -v   # 51 tests
black --check src tests          # code style check
```

## Troubleshooting

| Message | Cause | Solution |
|---|---|---|
| «введите целое число» | Non-numeric input | Enter an integer, e.g. `100` |
| «Значение должно быть неотрицательным» | Negative value | Enter a number ≥ 0 |
| «в файле … должно быть одно целое число» | File contains text or is empty | Provide a file with one integer |
| «не удалось прочитать файл …» | Missing or unreadable file | Check the path and permissions |
| «Ошибка записи в файл …» | Unwritable destination | Check the path and write permissions |
| «Ввод прерван пользователем.» | Ctrl+D / Ctrl+Z pressed | Run the program again |
| «Копия повреждена или отсутствует!» | Archive changed after creation | Use another archive or create a new one |

## Documentation

- [docs/ТЗ.md](docs/ТЗ.md) — technical specification (in Russian);
- [docs/Регламент_ТО.md](docs/Регламент_ТО.md) — maintenance regulations (in Russian);
- [docs/Тест-кейсы.md](docs/Тест-кейсы.md) — test cases (in Russian).
