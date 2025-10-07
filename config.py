import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-bem-dificil'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'outra-chave-secreta-mais-dificil-ainda'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'pokedex.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False