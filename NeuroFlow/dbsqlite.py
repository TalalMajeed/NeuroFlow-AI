from flask import Flask
import sqlite3
import os
import json
import base64
import string
import random
import datetime as dt

def connectSQL():
    try:
        print("Connecting to database")
        conn = sqlite3.connect('verceldb.db')
        conn.row_factory = sqlite3.Row
        return conn
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        conn = None

def createTables():
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            userID VARCHAR(5) PRIMARY KEY,
            name VARCHAR(45),
            gender VARCHAR(6),
            email VARCHAR(45),
            password VARCHAR(45),
            description VARCHAR(100),
            occupation VARCHAR(45),
            image BLOB,
            total INT
        )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS diagrams (
            diagramID VARCHAR(5) PRIMARY KEY,
            userID VARCHAR(5),
            name VARCHAR(45),
            description VARCHAR(100),
            data BLOB,
            date DATE,
            FOREIGN KEY (userID) REFERENCES users(userID)
        )''')
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn = None

createTables()

def codeGenerate():
    letters = string.ascii_lowercase
    numbers = string.digits
    code = ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(numbers) for i in range(3))
    return code.upper()


def getUsers():
    conn = connectSQL()
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
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        rows = cur.fetchall()
        cur.close()

        if len(rows) == 0:
            raise Exception("User not found")

        user_dict = None
        for row in rows:
            user_dict = row[0]

        return user_dict
    
    except Exception as e:
        print(f"Error: {e}")
        return -1


def getSQLUser(id):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userID = ?", (id,))
        rows = cur.fetchall()
        cur.close()

        if len(rows) == 0:
            raise Exception("User not found")

        for row in rows:
            if row[7]:
                image = row[7]
                image = base64.b64encode(image).decode('utf-8')
                image = base64.b64decode(image).decode('utf-8')
                image = f"data:image/png;base64,{image}"
            else:
                image = None
            user_dict = {'id': row[0], 'name': row[1], 'gender': row[2], 'email': row[3], 'description': row[5], 'image': image, 'occupation': row[6], 'total': row[8]}


        cur = conn.cursor()
        cur.execute("SELECT * FROM diagrams WHERE userID = ? ORDER BY date DESC", (id,))
        rows = cur.fetchall()
        cur.close()

        diagram_list = []
        for row in rows:
            diagram_dict = {'DiagramID': row[0], 'name': row[2], 'loading': False}
            diagram_list.append(diagram_dict)

        today = 0
        testDate = dt.date.today()

        for row in rows:
            print(row)
            if row[5] == testDate:
                print("INDEXING: " + str(row[5]))

                temp = row[4]
                temp = base64.b64encode(temp).decode('utf-8')
                temp = base64.b64decode(temp).decode('utf-8')
                temp = json.loads(temp)

                if temp != [[], []]:
                    today += 1

        user_dict['diagramCount'] = len(diagram_list)
        user_dict['today'] = today

        if len(diagram_list) > 2:
            diagram_list = diagram_list[:2]

        user_dict['diagrams'] = diagram_list
        return json.dumps(user_dict)
    
    except Exception as e:
        print(f"Error: {e}")
        return -1


def getSQLRecent(id):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM diagrams WHERE userID = ? ORDER BY date DESC LIMIT 2", (id,))
        rows = cur.fetchall()
        cur.close()

        diagram_list = []
        for row in rows:
            diagram_dict = {'DiagramID': row[0], 'name': row[2]}
            diagram_list.append(diagram_dict)

        return json.dumps(diagram_list)
    
    except Exception as e:
        print(f"Error: {e}")
        return -1


def checkIDSQL(id):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE userID = ?", (id,))
        rows = cur.fetchall()
        cur.close()

        if len(rows) == 0:
            return False

        user_dict = None
        for row in rows:
            user_dict = row[0]

        if user_dict == id:
            return True
        return False
    
    except Exception as e:
        print(f"Error: {e}")
    return False


def updateUser(userID, name, description, gender, occupation, image):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        if image:
            image = bytes(image.split(",")[1], "utf-8")
        else:
            image = None
        cur.execute("UPDATE users SET name = ?, description = ?, gender = ?, occupation = ?, image = ? WHERE userID = ?", (name, description, gender, occupation, image, userID))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1


def createSQLUser(email, password, name, gender, occupation):
    conn = connectSQL()
    try:
        print(email, password, name, gender, occupation)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        rows = cur.fetchall()
        cur.close()

        user_dict = None
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
        cur.execute("INSERT INTO users (userID, email, password, gender, name, occupation, total) VALUES (?, ?, ?, ?, ?, ?, 0)", (userID, email, password, gender, name, occupation))
        conn.commit()
        cur.close()

        return userID

    except Exception as e:
        print(f"Error: {e}")
        return -1


def deleteSQLUser(id):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE userID = ?", (id,))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1


def getSQLName(id):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE userID = ?", (id,))
        rows = cur.fetchall()
        cur.close()

        for row in rows:
            user_dict = row[0]
    
        return user_dict
    
    except Exception as e:
        print(f"Error: {e}")
        return -1


def getSQLEmail(id):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT email FROM users WHERE userID = ?", (id,))
        rows = cur.fetchall()
        cur.close()

        for row in rows:
            user_dict = row[0]
    
        return user_dict
    
    except Exception as e:
        print(f"Error: {e}")
        return -1


def resetSQLPassword(id, password):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = ? WHERE userID = ?", (password, id))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1


def saveSQLInfo(id, description, image):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        if image:
            image = bytes(image.split(",")[1], "utf-8")
        else:
            image = None
        cur.execute("UPDATE users SET description = ?, image = ? WHERE userID = ?", (description, image, id))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1


def saveSQLDiagram(uid, data, title):
    print(uid, data, title)
    print("STARTING")
    id = codeGenerate()
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM diagrams WHERE diagramID = ?", (id,))
        rows = cur.fetchall()

        diagram_list = []
        for row in rows:
            diagram_dict = row[0]
            diagram_list.append(diagram_dict)

        print(diagram_list)

        while id in diagram_list:
            id = codeGenerate()

        print(id)

        # Convert data to BLOB
        if data:
            data = json.dumps(data)
            data = bytes(data, "utf-8")
        else:
            data = None

        print(data)

        cur = conn.cursor()
        cur.execute("INSERT INTO diagrams (diagramID, userID, name, data, date) VALUES (?, ?, ?, ?, CURRENT_DATE)", (id, uid, title, data))
        conn.commit()
        cur.close()

        return id
    except Exception as e:
        print(f"Error: {e}")
        return -1


def updateSQLDiagram(did, data, title):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM diagrams WHERE diagramID = ?", (did,))
        rows = cur.fetchall()

        diagram_list = []
        for row in rows:
            diagram_dict = row[0]
            diagram_list.append(diagram_dict)

        if did not in diagram_list:
            return -2

        # Convert data to BLOB
        if data:
            data = json.dumps(data)
            data = bytes(data, "utf-8")
        else:
            data = None

        cur = conn.cursor()
        cur.execute("UPDATE diagrams SET name = ?, data = ? WHERE diagramID = ?", (title, data, did))
        conn.commit()
        cur.close()

        return did
    except Exception as e:
        print(f"Error: {e}")
        return -1


def deleteSQLDiagram(did):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM diagrams WHERE diagramID = ?", (did,))
        rows = cur.fetchall()

        diagram_list = []
        for row in rows:
            diagram_dict = row[0]
            diagram_list.append(diagram_dict)

        if did not in diagram_list:
            return -2

        cur = conn.cursor()
        cur.execute("DELETE FROM diagrams WHERE diagramID = ?", (did,))
        conn.commit()
        cur.close()

        return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1


def getSQLDiagrams(uid):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM diagrams WHERE userID = ?", (uid,))
        rows = cur.fetchall()
        cur.close()

        diagram_list = []
        for row in rows:
            diagram_dict = {'DiagramId': row[0], 'name': row[2]}
            diagram_list.append(diagram_dict)

        return json.dumps(diagram_list)
    
    except Exception as e:
        print(f"Error: {e}")
        return -1


def getSQLDiagram(did):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM diagrams WHERE diagramID = ?", (did,))
        rows = cur.fetchall()
        cur.close()

        for row in rows:
            if row[4]:
                data = row[4]
                data = base64.b64encode(data).decode('utf-8')
                data = base64.b64decode(data).decode('utf-8')
            else:
                data = None
            diagram_dict = {'DiagramId': row[0], 'name': row[2], 'data': data}
    
        print(diagram_dict)
        return json.dumps(diagram_dict)
    
    except Exception as e:
        print(f"Error: {e}")
        return -1


def increaseTotal(uid):
    conn = connectSQL()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET total = total + 1 WHERE userID = ?", (uid,))
        conn.commit()
        cur.close()
        return 1
    
    except Exception as e:
        print(f"Error: {e}")
        return -1