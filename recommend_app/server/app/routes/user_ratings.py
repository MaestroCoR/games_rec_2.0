from flask import Blueprint, request, jsonify, session
from app import db
from app.models import UserRating, User

from app.utils import login_required

bp = Blueprint('user_ratings', __name__, url_prefix='/user_ratings')


@bp.route('', methods=['GET'])
def get_user_ratings():
    ratings = UserRating.query.all()
    return jsonify([rating.to_dict() for rating in ratings])


@bp.route('/<int:user_id>', methods=['GET'])
def get_user_rating(user_id):
    user = User.query.get_or_404(user_id)
    ratings = user.ratings
    return jsonify([rating.to_dict() for rating in ratings])


@bp.route('/<int:game_id>', methods=['POST'])
@login_required
def create_user_rating(game_id):
    data = request.get_json()
    user_id = session.get('user_id')
    existing_rating = UserRating.query.filter_by(
        user_id=user_id, game_id=game_id).first()
    if existing_rating:
        existing_rating.rating = data['rating']
        db.session.commit()
        return jsonify(existing_rating.to_dict()), 201

    rating = UserRating(
        user_id=user_id, game_id=game_id, rating=data['rating'])
    db.session.add(rating)
    db.session.commit()
    return jsonify(rating.to_dict()), 201


@bp.route('/<int:game_id>', methods=['PUT'])
@login_required
def update_user_rating(game_id):
    user_id = session.get('user_id')
    rating = UserRating.query.filter_by(
        user_id=user_id, game_id=game_id).first_or_404()
    data = request.get_json()
    rating.rating = data.get('rating', rating.rating)
    db.session.commit()
    return jsonify(rating.to_dict())


@bp.route('/<int:game_id>', methods=['DELETE'])
@login_required
def delete_user_rating(game_id):
    user_id = session.get('user_id')
    rating = UserRating.query.filter_by(
        user_id=user_id, game_id=game_id).first_or_404()
    db.session.delete(rating)
    db.session.commit()
    return jsonify({'message': 'User rating deleted successfully'})
