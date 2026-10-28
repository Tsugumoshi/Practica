"""Автоматические тесты модуля backup_restore.py.

Каждый тест соответствует тест-кейсу из docs/Тест-кейсы.md; идентификатор
кейса указан в строке документации теста (например, TC-S-01).
Запуск: python -m unittest discover -v
"""

import hashlib
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import backup_restore as br  # noqa: E402


class ProjectFixtureMixin(unittest.TestCase):
    """Вспомогательное окружение: каталог проекта с типовыми файлами."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.project = self.base / "project"
        (self.project / "src").mkdir(parents=True)
        (self.project / "docs").mkdir()
        (self.project / "src" / "main.py").write_text(
            "print('hello')\n", encoding="utf-8"
        )
        (self.project / "docs" / "ТЗ.md").write_text(
            "# ТЗ\nУчебный проект.\n", encoding="utf-8"
        )
        self.backups = self.base / "backups"

    def tearDown(self):
        self._tmp.cleanup()


class Sha256FileTests(unittest.TestCase):
    """Тест-кейсы функции sha256_file(path)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_known_hash(self):
        """TC-S-01: для файла «abc» — известная контрольная сумма SHA-256."""
        path = self.dir / "a.txt"
        path.write_text("abc", encoding="utf-8")
        expected = hashlib.sha256(b"abc").hexdigest()
        self.assertEqual(br.sha256_file(path), expected)

    def test_different_content_different_hash(self):
        """TC-S-02: разное содержимое — разные суммы."""
        first = self.dir / "first.txt"
        second = self.dir / "second.txt"
        first.write_text("1", encoding="utf-8")
        second.write_text("2", encoding="utf-8")
        self.assertNotEqual(br.sha256_file(first), br.sha256_file(second))

    def test_empty_file_hash(self):
        """TC-S-03: пустой файл — сумма e3b0c442..."""
        path = self.dir / "empty.txt"
        path.write_bytes(b"")
        self.assertEqual(
            br.sha256_file(path),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )

    def test_deterministic(self):
        """TC-S-04: одинаковые файлы — одинаковые суммы."""
        first = self.dir / "one.txt"
        second = self.dir / "two.txt"
        first.write_text("данные", encoding="utf-8")
        second.write_text("данные", encoding="utf-8")
        self.assertEqual(br.sha256_file(first), br.sha256_file(second))

    def test_missing_file_raises(self):
        """TC-S-05: отсутствующий файл — FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            br.sha256_file(self.dir / "ghost.txt")


class CreateBackupTests(ProjectFixtureMixin):
    """Тест-кейсы функции create_backup(source_dir, backup_dir)."""

    def test_backup_created_with_manifest(self):
        """TC-B-01: копия создаётся, внутри есть manifest.sha256."""
        zip_path = br.create_backup(self.project, self.backups)
        self.assertTrue(zip_path.is_file())
        with zipfile.ZipFile(zip_path) as zf:
            self.assertIn("manifest.sha256", zf.namelist())

    def test_excluded_dirs_skipped(self):
        """TC-B-02: каталоги .git и __pycache__ не попадают в копию."""
        (self.project / ".git").mkdir()
        (self.project / ".git" / "config").write_text("git", encoding="utf-8")
        (self.project / "src" / "__pycache__").mkdir()
        (self.project / "src" / "__pycache__" / "m.pyc").write_bytes(b"cache")
        zip_path = br.create_backup(self.project, self.backups)
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        joined = " ".join(names)
        self.assertNotIn(".git/", joined)
        self.assertNotIn("__pycache__", joined)

    def test_existing_archive_not_overwritten(self):
        """TC-B-03: повторная копия — создаётся новый архив, старый не тронут."""
        first = br.create_backup(self.project, self.backups)
        second = br.create_backup(self.project, self.backups)
        self.assertNotEqual(first.name, second.name)
        self.assertTrue(first.is_file())
        self.assertTrue(second.is_file())

    def test_manifest_hashes_match_files(self):
        """TC-B-04: каждая строка манифеста — «SHA-256 путь» и сумма верна."""
        zip_path = br.create_backup(self.project, self.backups)
        with zipfile.ZipFile(zip_path) as zf:
            manifest = zf.read("manifest.sha256").decode("utf-8")
        for line in manifest.splitlines():
            hash_value, _, rel = line.partition(" ")
            with zipfile.ZipFile(zip_path) as zf:
                actual = hashlib.sha256(zf.read(rel)).hexdigest()
            self.assertEqual(actual, hash_value, rel)

    def test_missing_source_raises(self):
        """TC-B-05: несуществующий источник — FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            br.create_backup(self.base / "ghost", self.backups)


class VerifyBackupTests(ProjectFixtureMixin):
    """Тест-кейсы функции verify_backup(zip_path)."""

    def setUp(self):
        super().setUp()
        self.backups.mkdir(parents=True, exist_ok=True)

    def _make_backup(self) -> Path:
        return br.create_backup(self.project, self.backups)

    def test_valid_backup_passes(self):
        """TC-V-01: свежая копия — проверка возвращает True."""
        self.assertTrue(br.verify_backup(self._make_backup()))

    def test_tampered_file_fails(self):
        """TC-V-02: подмена файла внутри архива — False."""
        zip_path = self._make_backup()
        with zipfile.ZipFile(zip_path, "a") as zf:
            zf.writestr("src/main.py", "print('заменён')\n")
        self.assertFalse(br.verify_backup(zip_path))

    def test_missing_manifest_fails(self):
        """TC-V-03: архив без манифеста — False."""
        zip_path = self.backups / "no_manifest.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("src/main.py", "print('x')\n")
        self.assertFalse(br.verify_backup(zip_path))

    def test_missing_zip_fails(self):
        """TC-V-04: отсутствующий архив — False без исключения."""
        self.assertFalse(br.verify_backup(self.backups / "ghost.zip"))

    def test_corrupted_zip_fails(self):
        """TC-V-05: повреждённый архив (не ZIP) — False."""
        path = self.backups / "broken.zip"
        path.write_text("это точно не zip-архив", encoding="utf-8")
        self.assertFalse(br.verify_backup(path))


class RestoreBackupTests(ProjectFixtureMixin):
    """Тест-кейсы функции restore_backup(zip_path, dest_dir)."""

    def test_restore_identical_content(self):
        """TC-X-01: восстановленный каталог совпадает с исходным."""
        zip_path = br.create_backup(self.project, self.backups)
        dest = self.base / "restored"
        br.restore_backup(zip_path, dest)
        original = (self.project / "src" / "main.py").read_text(encoding="utf-8")
        restored = (dest / "src" / "main.py").read_text(encoding="utf-8")
        self.assertEqual(original, restored)

    def test_manifest_not_extracted(self):
        """TC-X-02: манифест не извлекается в каталог назначения."""
        zip_path = br.create_backup(self.project, self.backups)
        dest = self.base / "restored"
        br.restore_backup(zip_path, dest)
        self.assertFalse((dest / "manifest.sha256").exists())

    def test_path_traversal_rejected(self):
        """TC-X-03: запись с путём ../ — ValueError, выход за каталог закрыт."""
        zip_path = br.create_backup(self.project, self.backups)
        with zipfile.ZipFile(zip_path, "a") as zf:
            zf.writestr("manifest.sha256", "deadbeef ../../../evil.txt\n")
        with self.assertRaises(ValueError):
            br.restore_backup(zip_path, self.base / "restored")

    def test_tampered_backup_not_restored(self):
        """TC-X-04: повреждённая копия — ValueError, восстановление запрещено."""
        zip_path = br.create_backup(self.project, self.backups)
        with zipfile.ZipFile(zip_path, "a") as zf:
            zf.writestr("docs/ТЗ.md", "подменённое содержимое\n")
        with self.assertRaises(ValueError):
            br.restore_backup(zip_path, self.base / "restored")

    def test_restore_into_nested_new_dir(self):
        """TC-X-05: восстановление в новый вложенный каталог — создаётся."""
        zip_path = br.create_backup(self.project, self.backups)
        dest = self.base / "a" / "b" / "restored"
        br.restore_backup(zip_path, dest)
        self.assertTrue((dest / "docs" / "ТЗ.md").is_file())


class BackupRestoreMainTests(ProjectFixtureMixin):
    """Тест-кейсы функции backup_restore.main(argv)."""

    def _run(self, argv) -> int:
        with redirect_stdout(io.StringIO()) as _out:  # noqa: F841
            code = br.main(argv)
        return code

    def test_backup_command(self):
        """TC-K-01: команда backup — код 0 и созданный архив."""
        code = self._run(["backup", str(self.project), str(self.backups)])
        self.assertEqual(code, 0)
        archives = list(self.backups.glob("backup_*.zip"))
        self.assertEqual(len(archives), 1)

    def test_verify_valid_command(self):
        """TC-K-02: команда verify целостной копии — код 0."""
        zip_path = br.create_backup(self.project, self.backups)
        self.assertEqual(self._run(["verify", str(zip_path)]), 0)

    def test_verify_tampered_command(self):
        """TC-K-03: команда verify повреждённой копии — код 1."""
        zip_path = br.create_backup(self.project, self.backups)
        with zipfile.ZipFile(zip_path, "a") as zf:
            zf.writestr("src/main.py", "взломано\n")
        self.assertEqual(self._run(["verify", str(zip_path)]), 1)

    def test_restore_command(self):
        """TC-K-04: команда restore — код 0, файлы восстановлены."""
        zip_path = br.create_backup(self.project, self.backups)
        dest = self.base / "restored"
        self.assertEqual(self._run(["restore", str(zip_path), str(dest)]), 0)
        self.assertTrue((dest / "src" / "main.py").is_file())

    def test_verify_missing_file_command(self):
        """TC-K-05: verify отсутствующего архива — код 1, без трассировки."""
        self.assertEqual(self._run(["verify", str(self.backups / "ghost.zip")]), 1)


if __name__ == "__main__":
    unittest.main()
