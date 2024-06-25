import pandas as pd
import pymongo

# Підключення до MongoDB
mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mongo_db = mongo_client["steam_games"]
collection = mongo_db["user_played_games"]

# Створення списків для збереження даних
user_ids = []
game_ids = []
playtimes = []
user_counter = 0  # Лічильник збережених користувачів

# Отримання даних з MongoDB та їх збереження
for document in collection.find():
    if user_counter >= 10000:  # Обмеження до 10000 користувачів
        break

    if "games" in document and document["game_count"] > 0:
        steam_id = document["steam_id"]
        # Додаємо steam_id стільки разів, скільки ігор у користувача
        user_ids.extend([steam_id] * document["game_count"])
        games = document["games"]
        for game in games:
            game_ids.append(game["appid"])
            playtimes.append(game.get("playtime_forever", 0))

        user_counter += 1  # Збільшення лічильника користувачів

# Створення DataFrame з даними
data = {
    'steam_id': user_ids,
    'game_id': game_ids,
    'playtime_forever': playtimes
}
df = pd.DataFrame(data)

# Збереження у CSV файл
df.to_csv('user_game_data.csv', index=False)

# Закриття з'єднання та ресурсів
mongo_client.close()
