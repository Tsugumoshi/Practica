"""
Учебная практика ПМ.06. Вариант 1.
Сумма всех чётных элементов ряда Фибоначчи,
не превышающих заданное пользователем значение.

Режимы запуска:
    python fibonacci_even_sum.py                      - графический интерфейс (tkinter)
    python fibonacci_even_sum.py --console            - ввод через консоль
    python fibonacci_even_sum.py --input in.txt       - чтение предела из файла
    python fibonacci_even_sum.py --output out.txt     - запись результата в файл

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


def parse_limit(raw: str) -> int:
    """Преобразует введённую строку в целое число или выбрасывает ValueError."""
    raw = raw.strip()
    if not raw:
        raise ValueError("Введите предельное значение.")
    try:
        return int(raw)
    except ValueError:
        raise ValueError("Введите целое число без пробелов и точек.") from None


def format_result(limit: int, result: int) -> str:
    return f"Сумма чётных чисел Фибоначчи до {limit}: {result}"


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


def run_gui() -> None:
    """Графический интерфейс на tkinter (модуль подключается только здесь)."""
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title("Сумма чётных чисел Фибоначчи")
    root.geometry("700x420")
    root.minsize(500, 300)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = ttk.Frame(root, padding=16)
    frame.grid(sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    limit_var = tk.StringVar()
    result_var = tk.StringVar(value="Результат появится здесь")
    status_var = tk.StringVar()
    state = {"text": ""}

    def calculate() -> None:
        status_var.set("")
        try:
            limit = parse_limit(limit_var.get())
            result = even_fibonacci_sum(limit)
        except ValueError as exc:
            status_var.set(f"Ошибка: {exc}")
            return
        state["text"] = format_result(limit, result)
        result_var.set(state["text"])
        save_btn.config(state="normal")

    def load_from_file() -> None:
        path = filedialog.askopenfilename(
            title="Выберите файл с предельным значением",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                limit_var.set(f.read().strip())
        except OSError as exc:
            messagebox.showerror("Ошибка чтения файла", str(exc))
            return
        calculate()

    def save_to_file() -> None:
        if not state["text"]:
            return
        path = filedialog.asksaveasfilename(
            title="Сохранить результат", defaultextension=".txt",
            initialfile="result.txt", filetypes=[("Текстовые файлы", "*.txt")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(state["text"] + "\n")
        except OSError as exc:
            messagebox.showerror("Ошибка записи файла", str(exc))
            return
        messagebox.showinfo("Готово", f"Результат записан в {path}")

    def clear() -> None:
        limit_var.set("")
        status_var.set("")
        result_var.set("Результат появится здесь")
        state["text"] = ""
        save_btn.config(state="disabled")
        entry.focus()

    ttk.Label(frame, text="Предельное значение:").grid(row=0, column=0, sticky="w")
    entry = ttk.Entry(frame, textvariable=limit_var, width=60)
    entry.grid(row=1, column=0, columnspan=2, sticky="we", pady=(2, 10))
    entry.focus()

    ttk.Button(frame, text="Рассчитать", command=calculate).grid(
        row=2, column=0, sticky="we", padx=(0, 4))
    ttk.Button(frame, text="Загрузить из файла…", command=load_from_file).grid(
        row=2, column=1, sticky="we", padx=(4, 0))
    save_btn = ttk.Button(frame, text="Сохранить результат…",
                          command=save_to_file, state="disabled")
    save_btn.grid(row=3, column=0, sticky="we", padx=(0, 4), pady=(6, 0))
    ttk.Button(frame, text="Очистить", command=clear).grid(
        row=3, column=1, sticky="we", padx=(4, 0), pady=(6, 0))

    ttk.Separator(frame).grid(row=4, column=0, columnspan=2, sticky="we", pady=12)
    ttk.Label(frame, textvariable=result_var, wraplength=600,
              font=("TkDefaultFont", 14, "bold")).grid(row=5, column=0, columnspan=2, sticky="w")
    tk.Label(frame, textvariable=status_var, fg="#b00020", wraplength=600,
             justify="left").grid(row=6, column=0, columnspan=2, sticky="w", pady=(6, 0))

    root.bind("<Return>", lambda _e: calculate())
    root.mainloop()


def main() -> int:
    parser = argparse.ArgumentParser(description="Сумма чётных чисел Фибоначчи")
    parser.add_argument("--input", help="Файл с предельным значением")
    parser.add_argument("--output", help="Файл для записи результата")
    parser.add_argument("--console", action="store_true",
                        help="Ввод через консоль вместо графического интерфейса")
    args = parser.parse_args()

    # Без аргументов запускается графический интерфейс.
    if not (args.input or args.output or args.console):
        try:
            run_gui()
        except ImportError as exc:
            print(f"Ошибка: tkinter недоступен ({exc}). "
                  "Запустите программу с параметром --console.", file=sys.stderr)
            return 1
        return 0

    try:
        limit = read_limit_from_file(args.input) if args.input else read_limit_from_console()
        result = even_fibonacci_sum(limit)
    except (ValueError, OSError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1

    text = format_result(limit, result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Результат записан в {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
