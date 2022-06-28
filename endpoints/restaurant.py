
from db_helpers import run_query
import bcrypt
from flask import request, jsonify
from app import app
from patcher import restaurant_patcher
from verifyToken import token_validate

@app.route('/api/restaurant')
def get_restaurant_api():
    token = request.args.get('token')
    token_validate(token, 'restaurant')
    if not token_validate:
        return jsonify('invalid session')
    elif token_validate:
        
        restId = run_query('SELECT restaurantId from restaurant_session WHERE token=?', [token])
        restDataQuery = run_query('SELECT * from restaurant WHERE restaurantId =?', [restId[0][0]])
        restData = restDataQuery[0][:2] + restDataQuery[0][3:]
        return jsonify(restData)
    
@app.post('/api/restaurant')
def post_restaurant_api():

    salt = bcrypt.gensalt()
    data = request.json
    email = data.get('email')
    name = data.get('name')
    bio = data.get('bio')
    city = data.get('city')
    address= data.get('address')
    phone = data.get('phone')
    raw_pw = data.get('password')
    password = bcrypt.hashpw(raw_pw.encode(), salt)
    emailCheck = run_query("SELECT email FROM restaurant WHERE email = ?", [email])
    
    if not email or not password:

        return jsonify('Missing required field'), 422
    elif len(emailCheck) != 0:

        return jsonify('email already exists'), 422
    else:

        run_query("INSERT INTO restaurant (email, name, bio, address, city, phone_number, password) VALUES(?,?,?,?,?,?,?)", [email, name, address, bio, city, phone, password])
        return jsonify('added successfully')
    
@app.patch('/api/restaurant')
def patch_restaurant_api():
    data = request.json
    name = data.get('name')
    address = data.get('address')
    banner = data.get('banner')
    bio = data.get('bio')
    city = data.get('city')
    email = data.get('email')
    phone = data.get('phone')
    profile = data.get('profile')
    password = data.get('password')
    restaurantId = data.get('restaurantId')
    token = data.get('token')
    token_state = token_validate(token)
    if token_state:
        restaurant_patcher(name, address, banner, bio, city, email, phone, profile, password, restaurantId)
        return jsonify('patch was successful')
    else:
        return jsonify('Something went wrong')