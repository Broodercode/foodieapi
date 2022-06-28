import mariadb
from db_creds import *

def connect_db():
    conn=None
    cursor=None
    try:
        conn= mariadb.connect(host=host, port=port, database=database, user=user, password=password)
        cursor = conn.cursor()
        return (conn, cursor)
    except mariadb.OperationalError as e:
        print("got an operation error")
        if ("Access denied" in e.msg):
            print("failed to log in")
            disconnect_db()
    
def disconnect_db(conn,cursor):
    if (cursor != None):
        cursor.close()
    if (conn != None):
        conn.rollback()
        conn.close()
        
def run_query(statement, args=None):
    try:
        (conn, cursor) = connect_db()
        if statement.startswith("SELECT"):
            cursor.execute(statement, args)
            result = cursor.fetchall()
            print("Total of {} users".format(cursor.rowcount))
            return result
        else:
            cursor.execute(statement,args)
            if cursor.rowcount == 1:
                conn.commit()
                print("Query successful")
            else:
                print("Query failed")
        # except mariadb.OperationalError as e:
        # print("Got an operational error")
        # if ("Access denied" in e.msg):
        #     print("Failed to log in")

    # except mariadb.IntegrityError as e:
    #     print("Integrity error")
    #     if ("CONSTRAINT `user_CHECK_username`" in e.msg):
    #         print("Error, all usernames must start with the letter J")
    #     elif ("CONSTRAINT `users_CHECK_age`" in e.msg):
    #         print("Error, user is outside of acceptable age range")
    #     elif ("Duplicate entry" in e.msg):
    #         print("User already exists")
    #     else:
    #         print(e.msg)

    except mariadb.ProgrammingError as e:
        if ("SQL syntax" in e.msg):
            print("Syntax error")
        else:
            print("Got a different programming error")
        print(e.msg)

    except RuntimeError as e:
        print("Caught a runtime error")
        e.with_traceback

    except Exception as e:
        print(e.with_traceback)
        print(e.msg)

    finally:
        disconnect_db(conn,cursor)