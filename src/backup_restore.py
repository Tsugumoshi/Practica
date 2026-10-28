"""Резервное копирование и восстановление данных проекта.

Учебная практика ПМ.06 «Сопровождение информационных систем», вариант 1.

Схема: полное копирование проекта в ZIP-архив с меткой времени в имени
и манифестом контрольных сумм SHA-256. Перед восстановлением копия
обязательно проверяется на целостность.

Команды:
    python src/backup_restore.py backup  ИСТОЧНИК КАТАЛОГ_КОПИЙ
    python src/backup_restore.py verify  АРХИВ.zip
    python src/backup_restore.py restore АРХИВ.zip КАТАЛОГ_НАЗНАЧЕНИЯ

Используется только стандартная библиотека Python 3.10+.
"""

import argparse
import hashlib
import sys
import zipfile
from datetime import datetime
from pathlib import Path

# Имя файла манифеста внутри архива.
MANIFEST_NAME = "manifest.sha256"

# Служебные каталоги, которые не включаются в копию.
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", ".idea", ".vscode", "backups"}


def sha256_file(path: str | Path) -> str:
    """Вычислить контрольную сумму SHA-256 файла (шестнадцатеричная строка)."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _iter_project_files(source_dir: Path):
    """Перебрать файлы проекта, пропуская служебные каталоги."""
    for item in sorted(source_dir.rglob("*")):
        if not item.is_file():
            continue
        rel_parts = item.relative_to(source_dir).parts
        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue
        yield item


def create_backup(source_dir: str | Path, backup_dir: str | Path) -> Path:
    """Создать полную копию проекта в ZIP-архиве с манифестом SHA-256.

    Существующий архив не перезаписывается: к имени добавляется счётчик.
    Возвращает путь к созданному архиву. Для отсутствующего каталога
    источника выбрасывается FileNotFoundError.
    """
    source_dir = Path(source_dir)
    backup_dir = Path(backup_dir)
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Каталог источника не найден: {source_dir}")
    backup_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = backup_dir / f"backup_{stamp}.zip"
    counter = 1
    while zip_path.exists():
        zip_path = backup_dir / f"backup_{stamp}_{counter}.zip"
        counter += 1

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        manifest_lines = []
        for item in _iter_project_files(source_dir):
            rel = item.relative_to(source_dir).as_posix()
            zf.write(item, arcname=rel)
            manifest_lines.append(f"{sha256_file(item)} {rel}")
        zf.writestr(MANIFEST_NAME, "\n".join(manifest_lines) + "\n")
    return zip_path


def verify_backup(zip_path: str | Path) -> bool:
    """Проверить целостность копии.

    Копия считается целостной, если архив читается, состав файлов
    совпадает с манифестом и SHA-256 каждого файла совпадает с
    записанным. Возвращает True (копия целостна) или False.
    """
    zip_path = Path(zip_path)
    if not zip_path.is_file():
        return False
    try:
        with zipfile.ZipFile(zip_path) as zf:
            names = set(zf.namelist())
            if MANIFEST_NAME not in names:
                return False
            manifest_text = zf.read(MANIFEST_NAME).decode("utf-8")
            listed = {}
            for line in manifest_text.splitlines():
                if not line.strip():
                    continue
                hash_value, _, rel = line.partition(" ")
                listed[rel] = hash_value
            data_files = names - {MANIFEST_NAME}
            if data_files != set(listed):
                return False
            for rel, hash_value in listed.items():
                actual = hashlib.sha256(zf.read(rel)).hexdigest()
                if actual != hash_value:
                    return False
    except (zipfile.BadZipFile, UnicodeDecodeError, zipfile.LargeZipFile):
        return False
    return True


def restore_backup(zip_path: str | Path, dest_dir: str | Path) -> None:
    """Восстановить данные из копии в каталог назначения.

    Восстановление выполняется только после успешной проверки
    целостности. Пути записей контролируются, чтобы файл нельзя было
    распаковать за пределы каталога назначения. Манифест не извлекается.
    """
    zip_path = Path(zip_path)
    dest_dir = Path(dest_dir).resolve()
    if not verify_backup(zip_path):
        raise ValueError("Копия повреждена или не прошла проверку целостности")
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        for line in zf.read(MANIFEST_NAME).decode("utf-8").splitlines():
            if not line.strip():
                continue
            _hash, _, rel = line.partition(" ")
            target = (dest_dir / rel).resolve()
            if dest_dir != target and dest_dir not in target.parents:
                raise ValueError(f"Небезопасный путь в копии: {rel}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(rel))


def build_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="backup_restore",
        description="Резервное копирование и восстановление данных проекта.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_backup = sub.add_parser("backup", help="создать полную копию проекта")
    p_backup.add_argument("source", help="каталог-источник")
    p_backup.add_argument("backup_dir", help="каталог для копий")

    p_verify = sub.add_parser("verify", help="проверить целостность копии")
    p_verify.add_argument("zip_path", help="путь к архиву копии")

    p_restore = sub.add_parser("restore", help="восстановить данные из копии")
    p_restore.add_argument("zip_path", help="путь к архиву копии")
    p_restore.add_argument("dest_dir", help="каталог назначения")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Точка входа. Возвращает код завершения: 0 — успех, 1 — ошибка."""
    args = build_parser().parse_args(argv)
    try:
        if args.command == "backup":
            path = create_backup(args.source, args.backup_dir)
            print(f"Создана копия: {path}")
        elif args.command == "verify":
            if verify_backup(args.zip_path):
                print("Копия целостна.")
            else:
                print("Копия повреждена или отсутствует!")
                return 1
        elif args.command == "restore":
            restore_backup(args.zip_path, args.dest_dir)
            print(f"Данные восстановлены в каталог: {args.dest_dir}")
    except (OSError, ValueError) as exc:
        print(f"Ошибка: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
