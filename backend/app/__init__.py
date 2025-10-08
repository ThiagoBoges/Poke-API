from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        from . import models
        db.create_all()
        
    print("\n--- ROTAS REGISTRADAS ---")
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Métodos: {', '.join(rule.methods)}, Rota: {rule.rule}")
    print("-------------------------\n")
        
    return app