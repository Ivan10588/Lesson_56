import os
from pathlib import Path
import shutil
from datetime import datetime, timedelta
import zipfile


def archive_old_files(dir_path, day_threshold=30, archive_format='zip'):
    """
    Архивирует файлы старше day_threshold дней по дате последней модификации.
    Оригиналы остаются на месте (безопасный режим).
    
    Args:
        dir_path (str): путь к директории для сканирования.
        day_threshold (int): сколько дней считать «старым».
        archive_format (str): пока поддерживается 'zip'.
    """
    directory = Path(dir_path)

    if not directory.exists():
        print(f"Ошибка: путь '{dir_path}' не существует")
        return
    
    if not directory.is_dir():
        print(f"Ошибка: '{dir_path}' — это не папка")
        return

    cutoff_date = datetime.now() - timedelta(days=day_threshold)

    old_files = []
    for item in directory.iterdir():
        if not item.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
        except OSError:
            continue
        if mtime < cutoff_date:
            old_files.append((item, mtime))

    if not old_files:
        print("Нет файлов старше указанного порога для архивации.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"archive_{timestamp}.zip"
    archive_path = directory / archive_name

    print(f"Создаём архив: {archive_path}")
    print(f"Будет заархивировано файлов: {len(old_files)}")

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path, mtime in old_files:
            arcname = file_path.name
            zipf.write(file_path, arcname)
            print(f"  Добавлено: {file_path.name} (изменено: {mtime})")

    print(f"Архив успешно создан: {archive_path}")

def sort_files_by_extension(dir_path):
    """Сортирует файлы в указанной директории по расширению файла."""
    directory = Path(dir_path)

    if not directory.exists():
        print(f"Ошибка: путь '{dir_path}' не существует")
        return
    if not directory.is_dir():
        print(f"Путь {dir_path} должен быть до папки")
        return

    files = [item for item in directory.iterdir() if item.is_file()]
    if not files:
        print("В папке нет файлов для сортировки")
        return

    for item in files:
        ext = item.suffix.lower()[1:] or "no_extension"
        target_folder = directory / ext
        target_folder.mkdir(exist_ok=True)

        destination = target_folder / item.name
        orig_destination = destination
        counter = 1

        while destination.exists():
            stem = orig_destination.stem
            suffix = orig_destination.suffix
            destination = orig_destination.parent / f"{stem}_{counter}{suffix}"
            counter += 1

        shutil.move(item, destination)

    print("Сортировка завершена.")


if __name__ == "__main__":

    target_dir = "."  

    sort_files_by_extension(target_dir)

    archive_old_files(target_dir, day_threshold=7)
