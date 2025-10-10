#  Pokédex Digital  pokeball-emoji

Um projeto Full-Stack que implementa uma Pokédex interativa, permitindo que usuários se cadastrem, explorem uma lista de Pokémon e filtrem por tipo. O projeto foi construído com um back-end em Python (Flask) e um front-end em Angular.

## ✨ Funcionalidades

* **Autenticação de Usuários:** Sistema completo de registro e login com autenticação baseada em JSON Web Tokens (JWT).
* **Listagem de Pokémon:** Exibição dos 151 Pokémon da primeira geração em formato de cards.
* **Busca de Dados Detalhados:** Carregamento dinâmico de informações como stats (HP, Ataque, Defesa) e tipos de cada Pokémon.
* **Filtragem por Tipo:** Interface com botões para filtrar a lista de Pokémon exibida com base no seu tipo.
* **Navegação Protegida:** Utilização de Route Guards no Angular para proteger páginas que só podem ser acessadas por usuários logados.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias:

#### **Back-end**
* **Python 3**
* **Flask:** Framework principal da API.
* **Flask-SQLAlchemy:** ORM para interação com o banco de dados.
* **Flask-JWT-Extended:** Para gerenciamento de tokens de autenticação.
* **Flask-Cors:** Para permitir a comunicação entre o front-end e o back-end.
* **SQLite:** Banco de dados relacional.

#### **Front-end**
* **Angular 17+**
* **TypeScript**
* **SCSS:** Para estilização dos componentes.
* **Node.js & npm:** Para gerenciamento do ambiente de desenvolvimento front-end.

## 📂 Estrutura do Projeto

O repositório está organizado em uma estrutura de monorepo, com duas pastas principais:

` `` `
Poke-API/
├── 📂 backend/   # Contém toda a API em Python/Flask
└── 📂 frontend/  # Contém toda a aplicação em Angular
` `` `

## 🚀 Como Rodar o Projeto Localmente

Siga os passos abaixo para executar a aplicação na sua máquina.

### Pré-requisitos
* **Python** (versão 3.8 ou superior)
* **Node.js** e **npm** (versão LTS recomendada)
* **Angular CLI** (`npm install -g @angular/cli`)

### Back-end
1.  Abra um terminal e navegue até a pasta `backend`:
    ```bash
    cd backend
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
    # Use 'py' se 'python' não funcionar
    py -m venv venv
    source venv/Scripts/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Inicie o servidor (ele rodará em `http://localhost:8080`):
    ```bash
    py run.py
    ```

### Front-end
1.  Abra um **segundo terminal** e navegue até a pasta `frontend`:
    ```bash
    cd frontend
    ```
2.  Instale as dependências:
    ```bash
    npm install
    ```
3.  Inicie o servidor de desenvolvimento (ele rodará em `http://localhost:4200`):
    ```bash
    ng serve
    ```
4.  Acesse **`http://localhost:4200`** no seu navegador.

## 📖 Endpoints da API

| Método | Rota                  | Descrição                                
| :----- | :-------------------- | :----------------------------------------
| `POST` | `/register`           | Registra um novo usuário.                 
| `POST` | `/login`              | Autentica um usuário e retorna um token. 
| `GET`  | `/pokemons`           | Lista os Pokémon (com paginação).        
| `GET`  | `/types`              | Lista os tipos de Pokémon.                

## ✒️ Autor

Feito por **Thiago Borges**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ThiagoBoges)
