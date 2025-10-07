from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    dt_inclusao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

class PokemonUsuario(db.Model):
    id_pokemon_usuario = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    pokemon_id = db.Column(db.Integer, nullable=False) 
    nome = db.Column(db.String(100), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)
    favorito = db.Column(db.Boolean, default=False)
    grupo_batalha = db.Column(db.Boolean, default=False)
    __table_args__ = (db.UniqueConstraint('id_usuario', 'pokemon_id', name='_usuario_pokemon_uc'),)
    usuario = db.relationship('Usuario', backref='pokemons')