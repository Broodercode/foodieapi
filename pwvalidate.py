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

    print(user_session)
    print(handle_type)
    print(username)
    print(userCheck)
    if len(userCheck) == 1:
        print('inner pw checker')
        if user_session == 'restaurant':
            pw_validate = run_query("SELECT password FROM restaurant WHERE ?=?", [handle_type, username])
        elif user_session == 'clients':
            pw_validate = run_query("SELECT password FROM clients WHERE ?=?", [handle_type, username])
        else:
            print('something went wrong')
        print('after else inner pw')
        print(pw_validate)
        stored_pw = pw_validate[0][0]
        print(stored_pw.encode())
        print(bcrypt.checkpw(password.encode(), stored_pw.encode()))
        if bcrypt.checkpw(password.encode(), stored_pw.encode()):
            return True
        else:
            return False
