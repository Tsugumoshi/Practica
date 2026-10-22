# Practica
# Учебная практика ПМ.06 «Сопровождение информационных систем»

**Студент:** Абрамов Илья Сергеевич
**Курс:** 3
**Группа:** ИСП-31с
**Специальность:** 09.02.07 «Информационные системы и программирование»
**Период практики:** 19.10.2026 – 31.10.2026
**Объём:** 72 часа

## Вариант 1

Консольная программа на языке Python для нахождения **суммы всех чётных элементов ряда Фибоначчи, которые не превышают указанное пользователем значение**, с вводом/выводом через консоль и через файл.

## Состав репозитория

| Файл | Назначение |
|------|-----------|
| `fibonacci_even_sum.py` | Основная программа |
| `ТЗ.md` | Техническое задание |
| `Регламент_ТО.md` | Регламент технического обслуживания |
| `README.md` | Описание проекта (RU + EN) |

## Запуск

```bash
python fibonacci_even_sum.py
```

Программа поддерживает:
- ввод значения-ограничителя из консоли;
- ввод из файла (аргумент `--input file.txt`);
- вывод результата в консоль или в файл (`--output result.txt`).

## Пример работы

```text
Введите предельное значение: 100
Сумма чётных чисел Фибоначчи до 100: 44
```

## Лицензия

Учебный проект, 2026.

---

# Educational Practice PM.06 "Information Systems Maintenance"

**Student:** Ilya Sergeevich Abramov
**Course:** 3
**Group:** ISP-31s
**Specialty:** 09.02.07 "Information Systems and Programming"
**Practice period:** 19.10.2026 – 31.10.2026
**Duration:** 72 hours

## Variant 1

A Python console program that calculates **the sum of all even Fibonacci numbers not exceeding a user-specified value**, with console and file input/output.

## Repository contents

| File | Purpose |
|------|---------|
| `fibonacci_even_sum.py` | Main program |
| `ТЗ.md` | Technical specification |
| `Регламент_ТО.md` | Maintenance regulation |
| `README.md` | Project description (RU + EN) |

## Usage

```bash
python fibonacci_even_sum.py
```

Supports:
- console input of the limit value;
- file input (`--input file.txt`);
- output to console or file (`--output result.txt`).

## Example

```text
Enter the limit value: 100
Sum of even Fibonacci numbers up to 100: 44
```

## License

Educational project, 2026.
