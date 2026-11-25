import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

app.config['JWT_SECRET_KEY'] = os.environ.get(
    'JWT_SECRET_KEY', 'clave-solo-para-pruebas-locales'
)
jwt = JWTManager(app)


def get_connection():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    return psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='games',
        user='postgres',
        password='secret'
    )
    
@app.route('/api/hola')
def hola():
    return jsonify({'mensaje': 'Hola desde Flask'})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Usuario y contraseña obligatorios'}), 400

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE username = %s', (data['username'],))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

    token = create_access_token(identity=user['username'])
    return jsonify({'access_token': token})


@app.route('/api/games', methods=['GET'])
def list_games():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM games ORDER BY id')
    games = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(games)


@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM games WHERE id = %s', (game_id,))
    game = cur.fetchone()
    cur.close()
    conn.close()

    if game is None:
        return jsonify({'error': 'Juego no encontrado'}), 404
    return jsonify(game)


@app.route('/api/games', methods=['POST'])
@jwt_required()
def create_game():
    data = request.get_json()

    if not data or not data.get('nombre'):
        return jsonify({'error': 'El nombre es obligatorio'}), 400

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        '''INSERT INTO games (nombre, anio, descripcion, imagen, enlace)
           VALUES (%s, %s, %s, %s, %s) RETURNING *''',
        (
            data['nombre'],
            data.get('anio'),
            data.get('descripcion', ''),
            data.get('imagen', ''),
            data.get('enlace', ''),
        )
    )
    new_game = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_game), 201


@app.route('/api/games/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    data = request.get_json()

    if not data or not data.get('nombre'):
        return jsonify({'error': 'El nombre es obligatorio'}), 400

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        '''UPDATE games
           SET nombre = %s, anio = %s, descripcion = %s,
               imagen = %s, enlace = %s
           WHERE id = %s RETURNING *''',
        (
            data['nombre'],
            data.get('anio'),
            data.get('descripcion', ''),
            data.get('imagen', ''),
            data.get('enlace', ''),
            game_id,
        )
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if updated is None:
        return jsonify({'error': 'Juego no encontrado'}), 404
    return jsonify(updated)


@app.route('/api/games/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM games WHERE id = %s', (game_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if deleted == 0:
        return jsonify({'error': 'Juego no encontrado'}), 404
    return jsonify({'mensaje': 'Juego eliminado'})


if __name__ == '__main__':
    app.run(debug=True)