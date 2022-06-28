import bcrypt
from db_helpers import run_query

def pw_validate(username, password, userType):
    if userType=='restaurant':
        user_session = 'restaurant'
        handle_type = 'email'
        userCheck = run_query("SELECT email FROM restaurant WHERE ?=?", [handle_type, username])
    elif userType=='clients':
        user_session = 'clients'
        handle_type = 'username'
        userCheck = run_query("SELECT username FROM clients WHERE ?=?", [handle_type, username])

    if len(userCheck) == 1:

        if user_session == 'restaurant':
            pw_validate = run_query("SELECT password FROM restaurant WHERE ?=?", [handle_type, username])
        elif user_session == 'clients':
            pw_validate = run_query("SELECT password FROM clients WHERE ?=?", [handle_type, username])
        else:
            print('something went wrong')
        stored_pw = pw_validate[0][0]

        if bcrypt.checkpw(password.encode(), stored_pw.encode()):
            return True
        else:
            return False
