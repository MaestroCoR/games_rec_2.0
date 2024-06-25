from flask import Blueprint, request, jsonify, session, redirect, url_for

from app.models import Game

from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import joblib

bp = Blueprint('recommend', __name__, url_prefix='/recommend')

pivot_table = pd.read_pickle('pivot_table.pkl')
knn = joblib.load('knn_model.pkl')
user_data = pd.read_csv('user_data.csv')


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


@bp.route('/games', methods=['POST'])
def recommend():
    data = request.get_json()
    game_ids = data['game_ids']  # Масив ID ігор

    # Отримання рекомендацій
    recommended_games = get_recommendations_knn(
        game_ids, pivot_table, user_data)

    recommended_games = [
        game for game in recommended_games if str(game) != 'nan']
    recommended_games = [
        game for game in recommended_games if game not in game_ids][:20]

    recommended_games_with_info = []
    for title in recommended_games:
        game_info = Game.query.filter_by(title=title).first()
        if game_info:
            recommended_games_with_info.append(game_info.to_dict())
        else:
            print(f"Інформацію про гру {title} не знайдено")
    response = {'recommendation': recommended_games_with_info}

    return jsonify(response)
