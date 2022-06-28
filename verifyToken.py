import uuid

from db_helpers import run_query

def new_client_token(username):
    token = str(uuid.uuid4())
    checkToken = run_query("SELECT token FROM client_session WHERE token = ?", [token])
    while len(checkToken) != 0:
        new_token = str(uuid.uuid4())
        token = new_token
        print('token already exists')
        checkToken = run_query("SELECT token FROM clients_session WHERE token = ?", [token])
    print('token created')
    client_id = run_query("SELECT clientId FROM clients WHERE username = ?", [username])
    clientId = client_id[0][0]
    run_query("INSERT INTO client_session (clientId, token) VALUES(?,?)", [clientId, token])
    return str(token)

def new_restaurant_token(email):
    token = str(uuid.uuid4())
    checkToken = run_query("SELECT token FROM restaurant_session WHERE token = ?", [token])
    while len(checkToken) != 0:
        new_token = str(uuid.uuid4())
        token = new_token
        print('token already exists')
        checkToken = run_query("SELECT token FROM restaurant_session WHERE token = ?", [token])
    restaurant_id = run_query("SELECT restaurantId FROM restaurant WHERE email = ?", [email])
    restaurantId = restaurant_id[0][0]    
    run_query("INSERT INTO restaurant_session (restaurantId, token) VALUES(?,?)", [restaurantId, token]) 
    return str(token)
   
def token_validate(token, userType):
    if userType=='restaurant':
        user_session = 'restaurant_session'
        tokenCheck = run_query("SELECT token FROM restaurant_session WHERE token = ?", [token])
    elif userType=='client':
        user_session = 'client_session'
        tokenCheck = run_query("SELECT token FROM client_session WHERE token = ?", [token])
    print(user_session)
    
    print(tokenCheck)
    if len(tokenCheck) == 1:
        print( 'token verified works')
        return True
    else:
        print('something went wrong')
        return False
    
def token_delete(token, sessionType):
    if sessionType == 'restaurant':
        tokenCheck = run_query("SELECT token FROM restaurant_session WHERE token = ?", [token])
    if sessionType == 'client':
        tokenCheck = run_query("SELECT token FROM client_session WHERE token = ?", [token])
    if len(tokenCheck) == 1:
        if sessionType == 'restaurant':
            print( 'token rest delete reached')
            run_query("DELETE FROM restaurant_session WHERE token = ?", [token])
            return True
        if sessionType == 'client':
            run_query("DELETE FROM client_session WHERE token = ?", [token])
        else:
            return 'something went wrong'
        
        return True
    else:
        print('user not logged in')
        return False