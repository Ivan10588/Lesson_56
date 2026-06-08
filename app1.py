import os
from pathlib import Path

def rename_files(dir_path, old_pattern, new_pattern):
    """
    Переименовать файлы в директории, содержащие в имени old_pattern.
    
    Args:
        dir_path (str): путь к директории.
        old_pattern (str): подстрока, которую нужно искать в имени файла.
        new_pattern (str): подстрока, на которую нужно заменить old_pattern.
    """
    directory = Path(dir_path)

    # Проверка валидности пути
    if not directory.exists():
        print(f"Ошибка: путь '{dir_path}' не существует")
        return
    
    if not directory.is_dir():
        print(f"Ошибка: '{dir_path}' — это не папка")
        return

    # Собираем все файлы в папке
    files = [item for item in directory.iterdir() if item.is_file()]

    if len(files) == 0:
        print("В папке нет файлов для переименования")
        return

    renamed_count = 0

    for item in files:
        old_name = item.name
        
        # Ищем old_pattern в имени файла (без учета расширения)
        if old_pattern in old_name:
            # Формируем новое имя
            new_name = old_name.replace(old_pattern, new_pattern)
            new_path = item.parent / new_name
            
            # Переименовываем (move работает и для переименования внутри папки)
            item.rename(new_path)
            renamed_count += 1
            print(f"Переименовано: {old_name} -> {new_name}")

    print(f"Всего переименовано файлов: {renamed_count}")


# Пример использования (как в вашем скриншоте)
old_prefix = "IMG_"
new_prefix = "Vacation_Photo_"

# Вызываем функцию
rename_files("files", old_prefix, new_prefix)
