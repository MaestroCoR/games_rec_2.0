
from sklearn.neighbors import NearestNeighbors
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gaming_companion'
    # 'password': 'parol-dlya-mysql741',
    # 'database': 'gaming_companion_api'
}
app = Flask(__name__)
# CORS(app)

CORS(app, resources={r"/*": {"origins": "*"}})
pivot_table = pd.read_pickle('pivot_table.pkl')
knn = joblib.load('knn_model.pkl')
user_data = pd.read_csv('user_data.csv')


def get_gameId_by_title(title):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        sql_query = "SELECT gameId FROM games WHERE title LIKE %s"
        cursor.execute(sql_query, (f'%{title}%',))
        game_id = cursor.fetchone()
        cursor.close()
        db.close()
        return game_id[0] if game_id else None
    except Exception as e:
        print(f"Помилка: {str(e)}")
        return None


def get_game_info_by_title(title):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        sql_query = "SELECT title, steam_gameId, genres FROM games WHERE title = %s"
        cursor.execute(sql_query, (title,))
        game_info = cursor.fetchone()
        cursor.close()
        db.close()

        return game_info if game_info else None
    except Exception as e:
        print(f"Помилка: {str(e)}")
        return None


def get_recommendations_knn(game_ids, pivot_table, game_data):
    # Перевірка на цілі числа
    game_ids = [int(game_id)
                for game_id in game_ids if game_id is not None]
    print(game_ids)
    distances, indices = knn.kneighbors(pivot_table.iloc[game_ids].values)

    # Отримання рекомендацій з використанням індексів найближчих сусідів
    recommendations = []
    for i in range(len(indices)):
        similar_users = indices[i]
        for user_id in similar_users:
            recommended_games = game_data[game_data['userId'] == user_id].sort_values(
                'rating', ascending=False)['title'].values
            recommendations.extend(recommended_games)

    # Видалення дублікатів і повернення результату
    return list(dict.fromkeys(recommendations))


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    # game_names = data['game_ids']
    # print(game_names)
    game_ids = data['game_ids']  # Масив ID ігор
    print(game_ids)
    input_game_ids = game_ids
    # Отримання рекомендацій
    recommended_games = get_recommendations_knn(
        input_game_ids, pivot_table, user_data)

    recommended_games = [
        game for game in recommended_games if str(game) != 'nan']
    recommended_games = [
        game for game in recommended_games if game not in game_ids][:20]

    recommended_games_with_info = []
    for game in recommended_games:
        game_info = get_game_info_by_title(game)
        if game_info:
            title, steam_gameId, genres = game_info
            recommended_games_with_info.append({
                'title': title,
                'steam_gameId': steam_gameId,
                'genres': genres
            })
        else:
            print(f"Інформацію про гру {game} не знайдено")
    print(recommended_games)
    response = {'recommendation': recommended_games_with_info}

    return jsonify(response)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    limit = 5  # Обмеження кількості повернених ігор
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        sql_query = "SELECT gameId, title, steam_gameId, genres FROM games WHERE title LIKE %s LIMIT %s"
        cursor.execute(sql_query, (f'%{query}%', limit))
        games = cursor.fetchall()
        cursor.close()
        db.close()

        results = []
        for game in games:
            gameId, title, steam_gameId, genres = game
            results.append({
                'id': gameId,
                'title': title,
                'steam_gameId': steam_gameId,
                'genres': genres
            })

        return jsonify(results)
    except Exception as e:
        print(f"Помилка: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)
