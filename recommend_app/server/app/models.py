from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class ActivityLog(db.Model):
    __tablename__ = 'activity_log'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, nullable=True)
    entity_type = db.Column(db.String(50), nullable=True)
    action = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def to_dict_all(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'reviews': [review.to_dict() for review in self.reviews],
            'libraries': [library.to_dict() for library in self.libraries],
            'ratings': [rating.to_dict() for rating in self.ratings],
            'wishlists': [wishlist.to_dict() for wishlist in self.wishlists]
        }


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    genres = db.Column(db.String(100), nullable=True)
    release_date = db.Column(db.String(20), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    detailed_description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'steam_id': self.steam_id,
            'title': self.title,
            'genres': self.genres,
            'release_date': self.release_date,
            'short_description': self.short_description,
            'detailed_description': self.detailed_description,
            'ratings': [rating.to_dict() for rating in self.ratings],
            'reviews': [review.to_dict() for review in self.reviews]
        }

    def to_dict_preview(self):
        return {
            'id': self.id,
            'steam_id': self.steam_id,
            'title': self.title,
            'genres': self.genres,
            'release_date': self.release_date,
            'short_description': self.short_description
        }


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    game = db.relationship('Game', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'game_id': self.game_id,
            'review_text': self.review_text,
            'rating': self.rating,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user': self.user.to_dict(),
        }


class UserLibrary(db.Model):
    __tablename__ = 'user_libraries'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        'games.id'), primary_key=True)
    added_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('libraries', lazy=True))
    game = db.relationship('Game', backref=db.backref('libraries', lazy=True))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'game_id': self.game_id,
            'added_at': self.added_at,
            'game': self.game.to_dict_preview()
        }


class UserRating(db.Model):
    __tablename__ = 'user_ratings'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        'games.id'), primary_key=True)
    rating = db.Column(db.SmallInteger, nullable=False)
    rated_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    game = db.relationship('Game', backref=db.backref('ratings', lazy=True))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'game_id': self.game_id,
            'rating': self.rating,
            'rated_at': self.rated_at
        }


class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        'games.id'), primary_key=True)
    added_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('wishlists', lazy=True))
    game = db.relationship('Game', backref=db.backref('wishlists', lazy=True))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'game_id': self.game_id,
            'added_at': self.added_at,
            'game': self.game.to_dict_preview()
        }
