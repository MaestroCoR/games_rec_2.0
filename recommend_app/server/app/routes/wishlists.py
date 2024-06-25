from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Wishlist, User

from app.utils import login_required

bp = Blueprint('wishlists', __name__, url_prefix='/wishlists')


@bp.route('', methods=['GET'])
def get_wishlists():
    wishlists = Wishlist.query.all()
    return jsonify([wishlist.to_dict() for wishlist in wishlists])


@bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_wishlist(user_id):
    user = User.query.get_or_404(user_id)
    wishlists = user.wishlists
    return jsonify([wishlist.to_dict() for wishlist in wishlists])


@bp.route('/<int:game_id>', methods=['POST'])
@login_required
def create_wishlist(game_id):
    user_id = session.get('user_id')
    wishlist = Wishlist(
        user_id=user_id, game_id=game_id)

    db.session.add(wishlist)
    db.session.commit()
    return jsonify(wishlist.to_dict()), 201


@bp.route('/<int:game_id>', methods=['DELETE'])
@login_required
def delete_wishlist(game_id):
    user_id = session.get('user_id')
    wishlist = Wishlist.query.filter_by(
        user_id=user_id, game_id=game_id).first_or_404()

    db.session.delete(wishlist)
    db.session.commit()
    return jsonify({'message': 'Wishlist entry deleted successfully'})
