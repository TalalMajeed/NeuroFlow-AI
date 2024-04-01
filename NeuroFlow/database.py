from NeuroFlow.server import app
import psycopg2
import os

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
