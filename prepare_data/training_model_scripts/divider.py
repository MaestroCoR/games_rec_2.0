import json
import os

# Функція для розділення списку програм на менші частини


def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


# Кількість елементів у кожному файлі
chunk_size = 200000

# Підтримувані кодування, які можуть бути використані
encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']

for encoding in encodings:
    try:
        # Зчитування початкового JSON файлу з різними кодуваннями
        with open('Steam-1700265214487.json', 'r', encoding=encoding) as file:
            data = json.load(file)

        # Якщо файл успішно прочитано без помилок, виходимо з циклу
        break
    except UnicodeDecodeError:
        # Якщо виникла помилка декодування, спробуємо інше кодування
        continue
else:
    # Якщо жодне з кодувань не спрацювало, виведемо повідомлення про помилку
    print("Не вдалося правильно декодувати файл JSON.")

# Витягуємо список програм з файлу JSON
apps = data["applist"]["apps"]

# Розділення списку на менші частини
chunked_apps = list(chunk_list(apps, chunk_size))

# Створення папки для файлів, якщо вона не існує
output_folder = 'chunks200000'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Запис кожної частини у окремий JSON файл у створеній папці
for i, chunk in enumerate(chunked_apps):
    filename = os.path.join(output_folder, f"chunk_{i + 1}.json")
    with open(filename, "w", encoding='utf-8') as file:  # Вказання кодування для запису
        json.dump({"applist": {"apps": chunk}}, file, indent=4)

print("Розділення завершено.")
