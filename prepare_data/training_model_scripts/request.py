import json
import requests
import pymongo
import time

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client.steam_games
collection = db.games_details

with open('chunk_1.json', 'r') as file:
    json_data = json.load(file)

base_url = "http://store.steampowered.com/api/appdetails?appids="

for app in json_data['applist']['apps']:
    app_id = app['appid']

    # Перевірка чи є id у базі даних перед додаванням
    if collection.find_one({"app_id": app_id}):
        print(f"Гра з appid {app_id} вже є у базі даних, пропускаємо...")
        continue

    url = f"{base_url}{app_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            game_data = response.json()
            data_to_insert = {"app_id": app_id}
            data_to_insert.update(game_data.get(str(app_id), {}))

            collection.insert_one(data_to_insert)
            print(f"Дані для гри з appid {app_id} збережено у MongoDB")
            time.sleep(1.5)
        except json.decoder.JSONDecodeError as e:
            print(f"Помилка розшифровки JSON: {e}")

    else:
        print(f"Помилка отримання даних для гри з appid {app_id}")
        time.sleep(10)
client.close()
