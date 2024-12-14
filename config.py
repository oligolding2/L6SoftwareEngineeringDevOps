from dotenv import load_dotenv
import os

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV','production'),
    SECRET_KEY=os.environ.get('SECRET_KEY',os.urandom(24)),
    DATABASE_URL= os.environ.get('DATABASE_URL','/static/database.db'),
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE',True),
    SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY',True),
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE','Lax')
