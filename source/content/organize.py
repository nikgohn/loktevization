import os
import re
import shutil
import argparse
import sys

# -----------------------
# Разбор аргументов командной строки
# -----------------------
parser = argparse.ArgumentParser(
    description='Скрипт для организации изображений и нормализации ссылок в Markdown файлах.'
)
parser.add_argument(
    '--recheck',
    action='store_true',
    help='Проверить файлы в папке "files" на предмет использования в md файлах и переместить неиспользуемые в "unused".'
)
parser.add_argument(
    '--normalize',
    action='store_true',
    help='Нормализовать ссылки на изображения в md файлах, приводя их к виду ![[files/image.png]]. Другие операции не выполняются.'
)
args = parser.parse_args()

# -----------------------
# Если указан режим нормализации, выполняем только его и выходим
# -----------------------
if args.normalize:
    print("Запущен режим нормализации ссылок в Markdown файлах.")
    folder = '.'
    md_files = [f for f in os.listdir(folder) if f.endswith('.md')]
    # Допустимые расширения изображений
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'}

    def normalize_image_link(link: str) -> str:
        """
        Приводит ссылку к виду с прямыми слэшами и сохраняет путь, например:
        "files\\image_o.png" -> "files/image_o.png"
        Возвращает нормализованную ссылку, если расширение допустимо, иначе None.
        """
        norm = link.replace('\\', '/')
        ext = os.path.splitext(norm)[1].lower()
        if ext in image_extensions:
            return norm
        return None

    # Регулярное выражение для Markdown-ссылок: ![текст](ссылка)
    md_link_pattern = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
    # Регулярное выражение для Wiki-ссылок: ![[ссылка]] (возможно, с параметрами после |)
    wiki_link_pattern = re.compile(r'!\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]')

    def replace_md_link(match):
        link = match.group(1).strip()
        norm = normalize_image_link(link)
        if norm:
            return f"![[{norm}]]"
        else:
            return match.group(0)

    def replace_wiki_link(match):
        link = match.group(1).strip()
        norm = normalize_image_link(link)
        if norm:
            return f"![[{norm}]]"
        else:
            return match.group(0)

    for md_file in md_files:
        md_path = os.path.join(folder, md_file)
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Сначала обрабатываем Markdown-ссылки
        new_content = md_link_pattern.sub(replace_md_link, content)
        # Затем Wiki-ссылки
        new_content = wiki_link_pattern.sub(replace_wiki_link, new_content)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Нормализованы ссылки в файле: {md_file}")

    print("Нормализация завершена.")
    sys.exit(0)

# ------------------------------------------------------------------------------
# Если режим нормализации не включён, выполняется основная логика:
# 1. Перемещение изображений: упоминаемые в md-файлах – в папку "files", остальные – в "unused".
# 2. Обновление ссылок в md-файлах (приведение их к виду ![[files/image.png]]).
# 3. При параметре --recheck дополнительно проверяется папка "files".
# ------------------------------------------------------------------------------

folder = '.'
files_folder = os.path.join(folder, 'files')
unused_folder = os.path.join(folder, 'unused')

# Получаем список Markdown-файлов
md_files = [f for f in os.listdir(folder) if f.endswith('.md')]

# Допустимые расширения изображений
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'}

# Регулярные выражения для поиска ссылок на изображения:
# 1. Wiki-ссылки Obsidian: ![[имя_файла.ext]] или ![[имя_файла.ext|...]]
wiki_img_pattern = re.compile(r'!\[\[(.+?)\]\]')
# 2. Markdown-ссылки: ![](имя_файла.ext)
md_img_pattern = re.compile(r'!\[[^\]]*\]\((.+?)\)')

# Шаг 1. Сканирование Markdown-файлов: собираем имена изображений, на которые есть ссылки
referenced_images = set()
for md_file in md_files:
    with open(os.path.join(folder, md_file), 'r', encoding='utf-8') as f:
        content = f.read()
    # Обработка Wiki-ссылок: берём всё содержимое внутри ![[...]] и оставляем только часть до "|" если она есть
    for match in wiki_img_pattern.findall(content):
        image_ref = match.split('|')[0].strip()
        referenced_images.add(image_ref)
    # Обработка Markdown-ссылок
    for match in md_img_pattern.findall(content):
        image_ref = match.split()[0].strip()
        referenced_images.add(image_ref)

# Шаг 2. Получаем список всех изображений в рабочей папке
all_images = [f for f in os.listdir(folder)
              if os.path.isfile(f) and os.path.splitext(f)[1].lower() in image_extensions]

# Создаём папки "files" и "unused" (если их ещё нет)
os.makedirs(files_folder, exist_ok=True)
os.makedirs(unused_folder, exist_ok=True)

# Шаг 3. Перемещаем изображения: если файл упоминается – в "files", иначе – в "unused"
for img in all_images:
    src = os.path.join(folder, img)
    if img in referenced_images:
        dest = os.path.join(files_folder, img)
    else:
        dest = os.path.join(unused_folder, img)
    print(f"Перемещаем {img} -> {dest}")
    shutil.move(src, dest)

# Функция нормализации пути с заменой '\' на '/'
def normalize_path(path: str) -> str:
    return path.replace('\\', '/')

# Шаг 4. Обновляем ссылки в Markdown-файлах: приводим их к виду ![[files/image.png]]
def replace_wiki_link(match):
    inner = match.group(1)
    # Если присутствуют дополнительные параметры, оставляем только первую часть (имя файла с путем)
    parts = inner.split('|')
    file_path = parts[0].strip()
    # Если ссылка не содержит префикс "files/", а файл упоминается, добавляем его
    if not file_path.startswith('files/'):
        if file_path in referenced_images:
            file_path = os.path.join('files', file_path)
    # Приводим путь к нормальному виду (заменяем '\' на '/')
    norm = normalize_path(file_path)
    return f'![[{norm}]]'

def replace_md_link(match):
    link = match.group(1).strip()
    if not link.startswith('files/'):
        if link in referenced_images:
            link = os.path.join('files', link)
    norm = normalize_path(link)
    return f'![[{norm}]]'

for md_file in md_files:
    md_path = os.path.join(folder, md_file)
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = wiki_img_pattern.sub(replace_wiki_link, content)
    new_content = md_img_pattern.sub(replace_md_link, new_content)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Обновлены ссылки в {md_file}")

# Шаг 5. Если указан параметр --recheck, повторно проверяем файлы в папке "files"
if args.recheck:
    print("\nЗапущена повторная проверка файлов в папке 'files'...")
    # Перечитываем md-файлы для сбора ссылок после обновления
    recheck_references = set()
    for md_file in md_files:
        with open(os.path.join(folder, md_file), 'r', encoding='utf-8') as f:
            content = f.read()
        # Обработка Wiki-ссылок
        for match in wiki_img_pattern.findall(content):
            inner = match.split('|')[0].strip()
            if inner.startswith('files/'):
                inner = inner[len('files/'):]
            recheck_references.add(inner)
        # Обработка Markdown-ссылок
        for match in md_img_pattern.findall(content):
            link = match.strip()
            if link.startswith('files/'):
                link = link[len('files/'):]
            recheck_references.add(link)
    
    # Проверяем файлы в папке "files" — если файла нет среди ссылок, перемещаем его в "unused"
    for img in os.listdir(files_folder):
        img_path = os.path.join(files_folder, img)
        if os.path.isfile(img_path):
            if img not in recheck_references:
                dest = os.path.join(unused_folder, img)
                print(f"Recheck: перемещаем {img} из 'files' -> {dest}")
                shutil.move(img_path, dest)

print("\nСкрипт завершил работу.")
