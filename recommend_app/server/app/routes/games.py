from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app import db
from app.models import Game

from app.utils import login_required

bp = Blueprint('games', __name__, url_prefix='/games')


@bp.route('', methods=['GET'])
def get_games():
    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    title = request.args.get('title')

    query = Game.query

    if title:
        query = query.filter(Game.title.ilike(f'%{title}%'))

    # parse date from  and sort by release date
    # query = query.order_by(text("RIGHT(release_date, 4) DESC"))

    games = query.paginate(page=page, per_page=per_page)
    return jsonify({
        'games': [game.to_dict() for game in games.items],
        'total': games.total,
        'pages': games.pages,
        'page': games.page
    })


@bp.route('/<int:id>', methods=['GET'])
def get_game(id):
    game = Game.query.get_or_404(id)
    return jsonify(game.to_dict())


@bp.route('', methods=['POST'])
@login_required
def create_game():
    data = request.get_json()
    game = Game(
        title=data.get['title'],
        genres=data.get('genres'),
        release_date=data.get('release_date'),
        short_description=data.get('short_description'),
        detailed_description=data.get('detailed_description')
    )

    db.session.add(game)
    db.session.commit()
    return jsonify(game.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_game(id):
    game = Game.query.get_or_404(id)
    data = request.get_json()
    for key in data.keys():
        setattr(game, key, data[key])

    db.session.commit()
    return jsonify(game.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully'})
