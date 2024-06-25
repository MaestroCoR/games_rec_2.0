import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'mysql://root:parol-dlya-mysql741@localhost:3306/gaming_companion_api')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key')
    SESSION_COOKIE_SAMESITE = None
    SESSION_COOKIE_SECURE = False
