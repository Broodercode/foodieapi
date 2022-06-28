from app import app
from verifyToken import new_restaurant_token, token_validate, token_delete
from pwvalidate import pw_validate
from flask import request, jsonify

@app.post('/api/restaurant_login')
def restaurant_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_validated = pw_validate(email, password, 'restaurant')
    print('user validated')
    print(user_validated)
    token = new_restaurant_token(email)
    token_validate(token, 'restaurant')
    print(token)
    return jsonify(token)

@app.delete('/api/restaurant_login')
def restaurant_logout():
    data = request.json
    token = data.get('token')
    token_delete(token, 'restaurant')
    return jsonify('logout successful')