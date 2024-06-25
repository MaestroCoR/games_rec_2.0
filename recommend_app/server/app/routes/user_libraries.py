from flask import Blueprint, request, jsonify, session
from app import db
from app.models import UserLibrary, User
from app.utils import login_required

bp = Blueprint('user_libraries', __name__, url_prefix='/user_libraries')


@bp.route('', methods=['GET'])
@login_required
def get_current_user_library():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    libraries = user.libraries
    return jsonify([library.to_dict() for library in libraries])


@bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user_library(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != session.get('user_id'):
        return jsonify({'message': 'You are not authorized to view this library'}), 403
    libraries = user.libraries
    return jsonify([library.to_dict() for library in libraries])


@bp.route('/<int:game_id>', methods=['POST'])
@login_required
def add_game_to_user_library(game_id):
    user_id = session.get('user_id')

    library = UserLibrary(
        user_id=user_id, game_id=game_id)
    db.session.add(library)
    db.session.commit()
    return jsonify(library.to_dict()), 201


@bp.route('/<int:game_id>', methods=['DELETE'])
@login_required
def delete_game_from_user_library(game_id):
    user_id = session.get('user_id')
    library = UserLibrary.query.filter_by(
        user_id=user_id, game_id=game_id).first_or_404()
    db.session.delete(library)
    db.session.commit()
    return jsonify({'message': 'Game removed from library successfully'})
