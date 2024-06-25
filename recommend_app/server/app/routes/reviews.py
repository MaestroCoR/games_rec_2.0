from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Review

from app.utils import login_required

bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@bp.route('', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews])


@bp.route('/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get_or_404(id)
    return jsonify(review.to_dict())


@bp.route('', methods=['POST'])
@login_required
def create_review():
    data = request.get_json()
    review = Review(
        user_id=session.get('user_id'),
        game_id=data['game_id'],
        review_text=data['review_text'],
        rating=data['rating'])
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_review(id):
    review = Review.query.get_or_404(id)
    if review.user_id != session.get('user_id'):
        return jsonify({'message': 'You are not authorized to update this review'}), 403
    data = request.get_json()
    for key in data.keys():
        setattr(review, key, data[key])
    db.session.commit()
    return jsonify(review.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    if review.user_id != session.get('user_id'):
        return jsonify({'message': 'You are not authorized to delete this review'}), 403
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'})
