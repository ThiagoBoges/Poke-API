from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests
from . import db
from .models import Usuario, PokemonUsuario

main = Blueprint('main', __name__)
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

@main.route('/')
def index():
    return jsonify({"status": "API da Pokédex está no ar!"})


@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if Usuario.query.filter_by(login=data['login']).first():
        return jsonify({"message": "Este login já está em uso."}), 409

    new_user = Usuario(nome=data['nome'], login=data['login'])
    new_user.set_password(data['senha'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Usuario.query.filter_by(login=data.get('login')).first()
    
    if user and user.check_password(data.get('senha')):
        print(">>> SUCESSO! Gerando token com ID em formato STRING.")

        access_token = create_access_token(identity=str(user.id_usuario))
        return jsonify(access_token=access_token)
    
    return jsonify({"message": "Credenciais inválidas"}), 401


@main.route('/pokemon/<name>', methods=['GET'])
@jwt_required()
def get_pokemon_detail(name):
    try:
        response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{name.lower()}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            return jsonify({"message": "Pokémon não encontrado"}), 404
        else:
            return jsonify({"message": "Erro ao contatar a PokéAPI"}), 500
    except requests.exceptions.RequestException:
        return jsonify({"message": "Erro de conexão com a PokéAPI"}), 503

@main.route('/pokemons', methods=['GET'])
@jwt_required()
def get_pokemons_list():
    """
    Busca uma lista paginada de Pokémon da PokéAPI.
    Esta rota é protegida e requer um token JWT.
    Exemplo de uso: /pokemons?limit=50&offset=0
    """
    limit = request.args.get('limit', 20)
    offset = request.args.get('offset', 0)

    try:
        pokeapi_url = f"{POKEAPI_BASE_URL}pokemon?limit={limit}&offset={offset}"
        response = requests.get(pokeapi_url)
        response.raise_for_status()

        pokemon_data = response.json()
        
        return jsonify(pokemon_data.get('results', []))

    except requests.exceptions.RequestException as e:
        return jsonify({"message": "Erro ao se conectar com a PokéAPI", "error": str(e)}), 503
        
    
@main.route('/user/favorites', methods=['POST'])
@jwt_required()
def toggle_favorite():
    """Adiciona ou remove um Pokémon da lista de favoritos do usuário."""
    data = request.get_json()
    if not data or 'pokemon_id' not in data or 'name' not in data:
        return jsonify({"message": "Dados faltando: 'pokemon_id' e 'name' são obrigatórios."}), 400

    current_user_id = get_jwt_identity()
    pokemon_id = data['pokemon_id']
    
    pokemon_user_entry = PokemonUsuario.query.filter_by(
        id_usuario=current_user_id, 
        pokemon_id=pokemon_id
    ).first()

    if pokemon_user_entry:
        pokemon_user_entry.favorito = not pokemon_user_entry.favorito
        message = "Status de favorito atualizado."
    else:
        new_entry = PokemonUsuario(
            id_usuario=current_user_id,
            pokemon_id=pokemon_id,
            nome=data['name'],
            imagem_url=data.get('imagem_url'),
            favorito=True
        )
        db.session.add(new_entry)
        message = "Pokémon adicionado aos favoritos."

    db.session.commit()
    return jsonify({"message": message})

@main.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Retorna a lista de Pokémon favoritos do usuário."""
    current_user_id = get_jwt_identity()

    favoritos = PokemonUsuario.query.filter_by(id_usuario=current_user_id, favorito=True).all()
    
    lista_favoritos = [
        {
            "pokemon_id": fav.pokemon_id,
            "nome": fav.nome,
            "imagem_url": fav.imagem_url
        } 
        for fav in favoritos
    ]
    
    return jsonify(lista_favoritos)

@main.route('/user/team', methods=['POST'])
@jwt_required()
def toggle_team_member():
    """Adiciona ou remove um Pokémon da equipe de batalha do usuário."""
    data = request.get_json()
    if not data or 'pokemon_id' not in data or 'name' not in data:
        return jsonify({"message": "Dados faltando: 'pokemon_id' e 'name' são obrigatórios."}), 400

    current_user_id = get_jwt_identity()
    pokemon_id = data['pokemon_id']
    
    pokemon_user_entry = PokemonUsuario.query.filter_by(
        id_usuario=current_user_id, 
        pokemon_id=pokemon_id
    ).first()

    if not pokemon_user_entry or not pokemon_user_entry.grupo_batalha:
        # Conta quantos Pokémon já estão na equipe
        team_count = PokemonUsuario.query.filter_by(id_usuario=current_user_id, grupo_batalha=True).count()
        if team_count >= 6:
            return jsonify({"message": "A equipe de batalha já está cheia (limite de 6 Pokémon)."}), 409 
    if pokemon_user_entry:
        pokemon_user_entry.grupo_batalha = not pokemon_user_entry.grupo_batalha
        message = "Status da equipe de batalha atualizado."
    else:
        new_entry = PokemonUsuario(
            id_usuario=current_user_id,
            pokemon_id=pokemon_id,
            nome=data['name'],
            imagem_url=data.get('imagem_url'),
            grupo_batalha=True
        )
        db.session.add(new_entry)
        message = "Pokémon adicionado à equipe de batalha."

    db.session.commit()
    return jsonify({"message": message})

@main.route('/user/team', methods=['GET'])
@jwt_required()
def get_team():
    """Retorna a equipe de batalha do usuário."""
    current_user_id = get_jwt_identity()

    team_members = PokemonUsuario.query.filter_by(id_usuario=current_user_id, grupo_batalha=True).all()
    
    lista_equipe = [
        {
            "pokemon_id": member.pokemon_id,
            "nome": member.nome,
            "imagem_url": member.imagem_url
        } 
        for member in team_members
    ]
    
    return jsonify(lista_equipe)