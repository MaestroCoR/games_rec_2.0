import json
import requests
import pymongo
import time

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client.steam_games
collection = db.user_played_games
limit = 99800
start = 0
base_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
api_key = '-hidden-'

with open('steamids.txt', 'r') as file:
    steam_ids = file.readlines()

for steam_id in steam_ids:
    if start >= limit:
        print("------------------------LIMIT-------------------------")
        break
    steam_id = steam_id.strip()  # Видалення пробілів

    # Перевірка чи є id у базі даних перед додаванням
    if collection.find_one({"steam_id": steam_id}):
        print(
            f"Ігри користувача з steamid {steam_id} вже є у базі даних, пропускаємо...")
        continue

    # Додайте ключ API до URL
    url = base_url.format(api_key=api_key, steam_id=steam_id)
    start += 1
    response = requests.get(url)

    if response.status_code == 200:
        try:
            user_games_data = response.json()
            data_to_insert = {"steam_id": steam_id}
            data_to_insert.update(user_games_data.get('response', {}))

            collection.insert_one(data_to_insert)
            print(
                f"Дані про ігри користувача з steamid {steam_id} збережено у MongoDB")
            # time.sleep(0.25)
        except json.decoder.JSONDecodeError as e:
            print(f"Помилка розшифровки JSON: {e}")

    else:
        print(f"Помилка отримання даних для користувача з steamid {steam_id}")
        time.sleep(10)
client.close()
