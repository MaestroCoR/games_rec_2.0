# import csv
# from pymongo import MongoClient

# # Підключення до бази даних MongoDB
# mongo_client = MongoClient("mongodb://127.0.0.1:27017/")
# mongo_db = mongo_client["steam_games"]
# collection = mongo_db["games_details"]

# # Отримання даних з MongoDB колекції
# data_from_mongodb = list(collection.find())

# # Відкриття CSV файлу для запису
# with open('games.csv', mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['steam_id', 'title', 'genres',
#                   'release_date', 'short_description', 'detailed_description']
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     # Запис заголовків у CSV файл
#     writer.writeheader()

#     # Проходження через дані з MongoDB і запис даних в CSV файл
#     for item in data_from_mongodb:
#         if item.get('success', False):
#             game_data = item.get('data', {})
#             if all(key in game_data for key in ['steam_appid', 'type', 'name', 'release_date', 'short_description', 'detailed_description']):
#                 # Додаткова перевірка для збереження лише ігор
#                 if game_data['type'] == 'game':
#                     genres = ', '.join([genre['description']
#                                        for genre in game_data.get('genres', [])])
#                     release_date_info = game_data.get('release_date', {})
#                     # Перевірка структури release_date і збереження дати, якщо гра вже вийшла
#                     if not release_date_info.get('coming_soon', True):
#                         release_date = release_date_info.get('date')
#                         writer.writerow({
#                             'steam_id': game_data.get('steam_appid'),
#                             'title': game_data.get('name'),
#                             'genres': genres,
#                             'release_date': release_date,
#                             'short_description': game_data.get('short_description'),
#                             'detailed_description': game_data.get('detailed_description')
#                         })

#                 else:
#                     print(f"Not a game: {game_data.get('name')}")
#             else:
#                 print(f"Missing data for game: {game_data.get('name')}")
#         else:
#             print(f"Failed to load game: {item.get('app_id')}")

# print("CSV файл успішно створено з даними про ігри.")

import csv
from pymongo import MongoClient

# Підключення до бази даних MongoDB
mongo_client = MongoClient("mongodb://127.0.0.1:27017/")
mongo_db = mongo_client["steam_games"]
collection = mongo_db["games_details"]

# Отримання даних з MongoDB колекції
data_from_mongodb = list(collection.find())

# Фільтрація та сортування даних
filtered_and_sorted_data = sorted(
    [
        item.get('data') for item in data_from_mongodb
        if item.get('success', False) and item.get('data', {}).get('type') == 'game'
    ],
    key=lambda x: x.get('steam_appid')
)

# Відкриття CSV файлу для запису
with open('games.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['steam_id', 'title', 'genres',
                  'release_date', 'short_description', 'detailed_description']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Запис заголовків у CSV файл
    writer.writeheader()

    # Проходження через відсортовані дані і запис даних в CSV файл
    for game_data in filtered_and_sorted_data:
        if all(key in game_data for key in ['steam_appid', 'name', 'release_date', 'short_description', 'detailed_description']):
            genres = ', '.join([genre['description']
                               for genre in game_data.get('genres', [])])
            release_date_info = game_data.get('release_date', {})
            # Перевірка структури release_date і збереження дати, якщо гра вже вийшла
            if not release_date_info.get('coming_soon', True):
                release_date = release_date_info.get('date')
                writer.writerow({
                    'steam_id': game_data.get('steam_appid'),
                    'title': game_data.get('name'),
                    'genres': genres,
                    'release_date': release_date,
                    'short_description': game_data.get('short_description'),
                    'detailed_description': game_data.get('detailed_description')
                })

print("CSV файл успішно створено з даними про ігри.")
