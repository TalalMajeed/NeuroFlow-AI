from NeuroFlow.server import app
import psycopg2
import os
import json
import base64
import string
import random

conn = None

def connectSQL():
    global conn
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database='verceldb',
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        conn = None


def codeGenerate():
    letters = string.ascii_lowercase
    numbers = string.digits
    code = ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(numbers) for i in range(3))
    return code.upper()

def Query(f):
    def wrapper(*args, **kwargs):
        global conn
        try:
            if conn == None or conn.closed != 0:
                connectSQL()
        except Exception as e:
            print(f"Error connecting to database: {e}")
            conn = None
            return json.dumps({"status":500,"message":"Internal Server Error"})

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper

@Query
def getUsers():
    global conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cur.close()

    user_list = []
    for row in rows:
        user_dict = {'id': row[0], 'name': row[1]}
        user_list.append(user_dict)
    
    json_array = json.dumps(user_list)
    
    return json_array

@Query
def loginSQL(email, password):
    global conn
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        rows = cur.fetchall()
        cur.close()

        user_list = []
        for row in rows:
            user_dict = row[0]

        print(user_dict)
        return user_dict
    
    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def getSQLUser(id):
    global conn
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userID = %s", (id,))
        rows = cur.fetchall()
        cur.close()

        for row in rows:
            if row[6]:
                image = row[6]
                image = base64.b64encode(image).decode('utf-8')
                image = base64.b64decode(image).decode('utf-8')
                image = f"data:image/png;base64,{image}"
            else:
                image = None
            user_dict = {'id': row[0], 'name': row[1], 'gender':row[2], 'email': row[3],'description': row[5], 'image':image, 'occupation':row[7]}
    
        return json.dumps(user_dict)
    
    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def checkIDSQL(id):
    global conn
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userID = %s", (id,))
        rows = cur.fetchall()
        cur.close()

        user_list = []
        user_dict = None
        for row in rows:
            user_dict = row[0]

        if user_dict == id:
            return True
        return False
    
    except Exception as e:
        print(f"Error: {e}")
    return False

@Query
def updateUser(userID,name,description,gender,occupation,image):
    global conn
    try:
        cur = conn.cursor()
        if image:
            image = bytes(image.split(",")[1], "utf-8")
        else:
            image = None
        cur.execute("UPDATE users SET name = %s, description = %s, gender = %s, occupation = %s, image = %s WHERE userID = %s", (name, description, gender, occupation, image, userID))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def createSQLUser(email, password, name, gender, occupation):
    global conn
    try:
        print(email, password,name,gender,occupation)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        rows = cur.fetchall()
        cur.close()

        user_dict = []
        for row in rows:
            user_dict = row[0]

        if user_dict:
            return -2

        cur = conn.cursor()
        cur.execute("SELECT userID FROM users")
        rows = cur.fetchall()
        cur.close()

        user_list = []
        for row in rows:
            user_dict = row[0]
            user_list.append(user_dict)

        userID = ""
        while True:
            userID = codeGenerate()
            if userID not in user_list:
                break

        cur = conn.cursor()
        cur.execute("INSERT INTO users (userID, email, password, gender, name, occupation) VALUES (%s, %s, %s, %s, %s, %s)", (userID, email, password, gender, name, occupation))

        conn.commit()
        cur.close()

        return userID

    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def deleteSQLUser(id):
    global conn
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE userID = %s", (id,))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def getSQLName(id):
    global conn
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE userID = %s", (id,))
        rows = cur.fetchall()
        cur.close()

        for row in rows:
            user_dict = row[0]
    
        return user_dict
    
    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def getSQLEmail(id):
    global conn
    try:
        cur = conn.cursor()
        cur.execute("SELECT email FROM users WHERE userID = %s", (id,))
        rows = cur.fetchall()
        cur.close()

        for row in rows:
            user_dict = row[0]
    
        return user_dict
    
    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def resetSQLPassword(id, password):
    global conn
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = %s WHERE userID = %s", (password, id))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1

@Query
def saveSQLInfo(id, description, image):
    global conn
    try:
        cur = conn.cursor()
        if image:
            image = bytes(image.split(",")[1], "utf-8")
        else:
            image = None
        cur.execute("UPDATE users SET description = %s, image = %s WHERE userID = %s", (description, image, id))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1