from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
cors = CORS(supports_credentials=True, origins='http://localhost:5173')


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    from .routes import auth, recommend, games, reviews, user_libraries, user_ratings, wishlists

    app.register_blueprint(auth.bp)
    app.register_blueprint(recommend.bp)
    app.register_blueprint(games.bp)
    app.register_blueprint(reviews.bp)
    app.register_blueprint(user_libraries.bp)
    app.register_blueprint(user_ratings.bp)
    app.register_blueprint(wishlists.bp)

    return app
