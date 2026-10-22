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
| `README.md` | Описание проекта и подробное руководство пользователя |

---

## 📖 ПОДРОБНОЕ РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ

Данное руководство предназначено для пользователей, которые хотят запустить программу на своем компьютере. Программа не требует установки сторонних библиотек, так как использует только стандартные средства Python.

### 1. Системные требования
* **Операционная система:** Windows 10/11, macOS, Linux.
* **Среда разработки:** Python версии 3.10 или выше.
* **Свободное место на диске:** не менее 10 МБ.

### 2. Подготовка к работе (Установка)
1. **Установите Python:** Если у вас не установлен Python, скачайте его с официального сайта [python.org](https://www.python.org/downloads/).
   * *Важно для Windows:* при установке обязательно поставьте галочку **«Add Python to PATH»** в самом первом окне установщика.
2. **Скачайте проект:** Нажмите зеленую кнопку **«Code»** в верхней части страницы GitHub и выберите **«Download ZIP»**.
3. **Распакуйте архив:** Извлеките файлы из ZIP-архива в любую удобную папку на вашем компьютере (например, на Рабочий стол).

### 3. Способы запуска программы
Откройте терминал (командную строку), перейдите в папку с проектом (используйте команду `cd путь_к_папке`) и используйте один из следующих режимов:

**Режим 1. Интерактивный (ввод вручную)**
Запустите программу командой:
```bash
python fibonacci_even_sum.py
```
Программа попросит ввести число. Введите целое число (например, `100`) и нажмите Enter. Результат появится на экране.

**Режим 2. Чтение из файла (автоматический)**
Если вы хотите брать число из файла:
1. Создайте текстовый файл `input.txt` в папке с программой.
2. Напишите в нем одно число (например, `1000`) и сохраните.
3. Запустите программу с аргументом `--input`:
```bash
python fibonacci_even_sum.py --input input.txt
```

**Режим 3. Запись результата в файл**
Если вы хотите сохранить ответ в файл, используйте аргумент `--output`:
```bash
python fibonacci_even_sum.py --output result.txt
```
После ввода числа (или чтения из файла) ответ запишется в `result.txt`, а в консоль выведется сообщение об успехе.

**Режим 4. Комбинированный**
Можно читать из одного файла и писать в другой:
```bash
python fibonacci_even_sum.py --input input.txt --output result.txt
```

### 4. Частые ошибки и способы их решения

| Ошибка в консоли | Причина | Как исправить |
| :--- | :--- | :--- |
| `python не является внутренней или внешней командой` | Python не установлен или не добавлен в PATH. | Переустановите Python, отметив галочку «Add Python to PATH». Либо используйте команду `py` вместо `python`. |
| `Ошибка: введите целое число.` | Вы ввели буквы, символы или дробное число. | Введите целое число без пробелов и точек (например, `500`). |
| `Ошибка: Значение должно быть неотрицательным` | Вы ввели число со знаком минус (например, `-10`). | Ряд Фибоначчи начинается с положительных чисел. Введите число `0` или больше. |
| `Ошибка: [Errno 2] No such file or directory` | Программа не может найти файл, указанный в `--input`. | Проверьте, что файл существует и находится в той же папке, откуда вы запускаете программу. |
| `SyntaxError: invalid syntax` | Используется очень старая версия Python. | Обновите Python до версии 3.10 или выше. |

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
| `README.md` | Project description and detailed user guide |

---

## 📖 DETAILED USER GUIDE

This guide is intended for users who want to run the program on their computer. The program does not require any third-party libraries, as it uses only standard Python features.

### 1. System Requirements
* **Operating System:** Windows 10/11, macOS, Linux.
* **Environment:** Python version 3.10 or higher.
* **Disk Space:** at least 10 MB.

### 2. Getting Started (Installation)
1. **Install Python:** If you don't have Python installed, download it from the official website [python.org](https://www.python.org/downloads/).
   * *Important for Windows:* during installation, make sure to check the **"Add Python to PATH"** box in the first installer window.
2. **Download the project:** Click the green **"Code"** button at the top of the GitHub page and select **"Download ZIP"**.
3. **Extract the archive:** Unzip the files to any convenient folder on your computer (e.g., your Desktop).

### 3. How to Run the Program
Open a terminal (command prompt), navigate to the project folder (use `cd path_to_folder`), and use one of the following modes:

**Mode 1. Interactive (Manual Input)**
Run the program using the command:
```bash
python fibonacci_even_sum.py
```
The program will prompt you to enter a number. Enter an integer (e.g., `100`) and press Enter. The result will appear on the screen.

**Mode 2. File Input (Automatic)**
If you want to read the number from a file:
1. Create a text file `input.txt` in the program folder.
2. Put a single number in it (e.g., `1000`) and save it.
3. Run the program with the `--input` argument:
```bash
python fibonacci_even_sum.py --input input.txt
```

**Mode 3. File Output**
If you want to save the result to a file, use the `--output` argument:
```bash
python fibonacci_even_sum.py --output result.txt
```
After entering a number (or reading from a file), the result will be written to `result.txt`, and a success message will be displayed in the console.

**Mode 4. Combined**
You can read from one file and write to another:
```bash
python fibonacci_even_sum.py --input input.txt --output result.txt
```

### 4. Troubleshooting

| Console Error | Cause | How to Fix |
| :--- | :--- | :--- |
| `python is not recognized as an internal or external command` | Python is not installed or not added to PATH. | Reinstall Python and check "Add Python to PATH". Alternatively, use the `py` command instead of `python`. |
| `Error: enter an integer.` | You entered letters, symbols, or a float number. | Enter an integer without spaces or dots (e.g., `500`). |
| `Error: Value must be non-negative` | You entered a negative number (e.g., `-10`). | The Fibonacci sequence starts with positive numbers. Enter `0` or a larger number. |
| `Error: [Errno 2] No such file or directory` | The program cannot find the file specified in `--input`. | Check that the file exists and is located in the same folder you are running the program from. |
| `SyntaxError: invalid syntax` | An outdated version of Python is being used. | Upgrade Python to version 3.10 or higher. |
