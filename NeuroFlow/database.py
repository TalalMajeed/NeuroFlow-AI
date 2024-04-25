from NeuroFlow.server import app
import psycopg2
import os
import json

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

def getUsers():
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

def loginSQL(email, password):
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

def getSQLUser(id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userID = %s", (id,))
        rows = cur.fetchall()
        cur.close()

        print(rows)

        for row in rows:
            user_dict = {'id': row[0], 'name': row[1], 'gender':row[2], 'email': row[3],'description': row[5]}
    
        return json.dumps(user_dict)
    
    except Exception as e:
        print(f"Error: {e}")
        return -1

def checkIDSQL(id):
    try:
        print("THIS IS FUNCTIONING")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userID = %s", (id,))
        rows = cur.fetchall()
        cur.close()

        print("sdfsefsefse")

        user_list = []
        for row in rows:
            user_dict = row[0]

        print("THIS FUNCTION IS FUNCTIONING")
        print(user_dict)
        if user_dict == id:
            return True
        return False
    
    except Exception as e:
        print(f"Error: {e}")
    return False