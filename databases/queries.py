from databases.connections import get_connection


# Validating and checking whether the admin exists in the table or not 
def validate_admin(username, password):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """-- sql
                SELECT * FROM admin 
                WHERE username = %s AND password = %s
            """
            cursor.execute(sql, (username, password))
            admin = cursor.fetchone()  # will return a single dictionary or None
            return admin 
    finally:
        conn.close()



#searching if any previous admin exists or not with the same (username)
def check_username_exists(username):
    conn=get_connection()
    try:
        with conn.cursor() as cursor:
            sql="""SELECT * FROM ADMIN 
                    WHERE USERNAME = %s"""
            cursor.execute(sql, (username,) )
            admin = cursor.fetchone() # return a single dictionary
            return admin
    finally:
        conn.close()
        
#ingestiing the user and password in database 
def insert_in_admin(username, password):
    conn=get_connection()
    try:
        with conn.cursor() as cursor:
            sql="""insert into admin
                    (username,password)
                    values
                    (%s,%s);"""
            cursor.execute(sql, (username,password))
            conn.commit()
            admin = cursor.lastrowid
            return admin
    finally:
        conn.close()