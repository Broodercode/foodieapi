from app import app

from verifyToken import new_client_token, token_validate, token_delete

from pwvalidate import pw_validate
from flask import request, jsonify

@app.post('/api/client_login')
def client_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_validated = pw_validate(username, password, 'clients')

    token = new_client_token(username)
    token_validate(token, 'client')

    return jsonify(token)

@app.delete('/api/client_login')
def client_logout():
    data = request.json
    token = data.get('token')
    token_validate(token)
    token_delete(token)
    return jsonify('logged out')