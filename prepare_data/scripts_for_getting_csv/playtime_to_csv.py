import pandas as pd
import pymongo

# Завантаження даних з games.csv
games_df = pd.read_csv('games.csv')
valid_game_ids = set(games_df['steam_id'].astype(int))

# Підключення до MongoDB
mongo_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mongo_db = mongo_client["steam_games"]
collection = mongo_db["user_played_games"]

# Створення списків для збереження даних
user_ids = []
game_ids = []
playtimes = []
user_counter = 0  # Лічильник збережених користувачів
user_id_map = {}  # Словник для збереження відповідності steam_id до порядкових номерів
next_user_id = 1  # Наступний доступний порядковий номер користувача

# Отримання даних з MongoDB та їх збереження
for document in collection.find():
    if user_counter >= 10000:  # Обмеження до 10000 користувачів
        break

    if "games" in document and document["game_count"] > 0:
        steam_id = document["steam_id"]
        if steam_id not in user_id_map:
            user_id_map[steam_id] = next_user_id
            next_user_id += 1

        user_id = user_id_map[steam_id]
        games = document["games"]
        filtered_games = [
            game for game in games if game["appid"] in valid_game_ids]

        if filtered_games:
            # Додаємо user_id стільки разів, скільки ігор у користувача після фільтрації
            user_ids.extend([user_id] * len(filtered_games))
            for game in filtered_games:
                game_ids.append(game["appid"])
                playtimes.append(game.get("playtime_forever", 0))

            user_counter += 1  # Збільшення лічильника користувачів

# Створення DataFrame з даними
data = {
    'user_id': user_ids,
    'game_id': game_ids,
    'playtime_forever': playtimes
}
df = pd.DataFrame(data)

# Збереження у CSV файл
df.to_csv('user_game_played_data.csv', index=False)

# Закриття з'єднання та ресурсів
mongo_client.close()
