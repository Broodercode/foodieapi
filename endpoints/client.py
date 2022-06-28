
from db_helpers import run_query
import bcrypt
from flask import request, jsonify
from app import app
from verifyToken import token_validate
from patcher import client_patcher


@app.route('/api/client', methods=['GET'])
def get_client_api():
    token = request.args.get('token')
    token_validate(token, 'client')
    
    if not token_validate:
        return jsonify('invalid session')
    elif token_validate:
            
        userId = run_query('SELECT clientId from client_session WHERE token = ?', [token])
        
        userDataQuery = run_query('SELECT * from clients WHERE clientId =?', [userId[0][0]])
        userData = userDataQuery[0][:3] + userDataQuery[0][4:]
        return jsonify(userData)

@app.post('/api/client')
def post_client_api():
    salt = bcrypt.gensalt()
    data = request.json
    email = data.get('email')
    username = data.get('username')
    raw_pw = data.get('password')
    password = bcrypt.hashpw(raw_pw.encode(), salt)
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    picture_url = data.get('pictureURL')
    print('post function reached')
    print(raw_pw)
    print(password)
    userCheck = run_query("SELECT username FROM clients WHERE username = ?" [username])
    emailCheck = run_query("SELECT email FROM clients WHERE email = ?" [email])
    
    print('username')
    print(username)
    print('usercheck')
    print(len(userCheck))
    print(userCheck)
    print(password)
    if not email or not username or not password:
        print('not function reached')
        return jsonify('Missing required field'), 422
    elif len(userCheck) != 0 or len(emailCheck) != 0:
        print('username or email already exists')
        return jsonify('username or email already exists'), 422
    
    else:
        print('query function reached')
        
        run_query("INSERT INTO clients (email, username, password, first_name, last_name, picture_url) VALUES(?,?,?,?,?,?)", [email, username, password, first_name, last_name, picture_url])
        return jsonify('added successfully')
    

@app.delete('/api/client')
def delete_client_api():
    print('delete client')

@app.patch('/api/client')
def patch_client_api():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    picture_url = data.get('pictureURL')
    token = data.get('token')
    print('token validate incoming')
    token_state = token_validate(token)
    print(token_state)
    if token_state:
        client_patcher(email, username, password, first_name, last_name, picture_url)
    else:
        return 'something went wrong'
    return jsonify('patch successful')

