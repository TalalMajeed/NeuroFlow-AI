from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
from flask_cors import CORS
import jwt
import datetime
import json
import ast


app = Flask(__name__)
CORS(app)

from NeuroFlow.database import *
from NeuroFlow.validation import *
from NeuroFlow.generator import *
from NeuroFlow.placement import *

waitingData = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def send_static(path):
    print("Requested path:", path)
    links = ["","login","panel","welcome","register","forgot","info"]
    if path in links:
        return render_template('index.html')
    else:
        return send_from_directory('static', path)

@app.route('/api')
def home():
    return "<h1>NeuroFlow API</h1><p>This site is a prototype API for NeuroFlow.</p>"

@app.route('/checkdb')
def checkdb():
    if conn is not None:
        return jsonify({"status": 200, "message": "Connected to database"})
    else:
        return jsonify({"status": 500, "message": "Error connecting to database"})

@app.route('/loginUser', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = loginSQL(email, password)
    

    if user == -1:
        return jsonify({"status": 401, "message": "Login failed"})
    else:
        token = jwt.encode({'uid': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret', algorithm='HS256')
        return jsonify({"status": 200, "message": "Login successful", "data": json.dumps({"uid": user, "token": token})})

    return jsonify({"status": 500, "message": "Internal Server Error"})

@app.route('/createUser', methods=['POST'])
def create():
    data = request.get_json()
    email = data['email']
    password = data['password']
    name = data['name']
    gender = data['gender']
    occupation = data['occupation']

    x = createSQLUser(email, password, name, gender, occupation)

    if x == -1:
        return jsonify({"status": 401, "message": "Registration failed"})
    elif x == -2:
        return jsonify({"status": 409, "message": "Email already registered"})
    else:
        token = jwt.encode({'uid': x, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret', algorithm='HS256')
        return jsonify({"status": 200, "message": "Registration successful", "data": json.dumps({"uid": x, "token": token})})

    return jsonify({"status": 500, "message": "Internal Server Error"})

@app.route('/checkauth', methods=['POST'])
@RequiredToken
def checkauth():
    x = getSQLUser(request.get_json()['uid'])
    if x == -1:
        return jsonify({"status": 401, "message": "Unauthorized"})
    return jsonify({"status": 200, "message": "Authorized", "data": x})

@app.route('/renew', methods=['POST'])
@RequiredToken
def renew():
    token = jwt.encode({'uid': request.get_json()['uid'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret', algorithm='HS256')
    return jsonify({"status": 200, "message": "Renew successful", "data": json.dumps({"uid": request.get_json()['uid'], "token": token})})

@app.route('/updateUser', methods=['POST'])
@RequiredToken
def update():
    data = request.get_json()

    x = updateUser(data['uid'], data['name'], data['description'], data['gender'], data['occupation'], data['image'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "User updated"})

@app.route('/deleteUser', methods=['POST'])
@RequiredToken
def delete():
    x = deleteSQLUser(request.get_json()['uid'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "User deleted"})

@app.route('/info', methods=['POST'])
@RequiredToken
def info():
    x = getSQLName(request.get_json()['uid'])
    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": x})

@app.route('/email', methods=['POST'])
@RequiredToken
def email():
    x = getSQLEmail(request.get_json()['uid'])
    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": x})

@app.route('/saveinfo', methods=['POST'])
@RequiredToken
def saveInfo():
    data = request.get_json()
    x = saveSQLInfo(data['uid'], data['description'],data['image'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "Info saved"})

@app.route('/reset', methods=['POST'])
@RequiredToken
def reset():
    data = request.get_json()
    x = resetSQLPassword(data['uid'], data['password'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "Password reset"})

@app.route('/savediagram', methods=['POST'])
@RequiredToken
def saveDiagram():
    data = request.get_json()

    if not data['did'] or data['did'] == "" or data['did'] == "Unsaved":
        x = saveSQLDiagram(data['uid'], data['data'],data['title'])
    else:
        x = updateSQLDiagram(data['did'], data['data'],data['title'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "Diagram Saved", "data": x})

@app.route('/deletediagram', methods=['POST'])
@RequiredToken
def deleteDiagram():
    data = request.get_json()
    x = deleteSQLDiagram(data['did'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "Diagram Deleted"})

@app.route('/getdiagrams', methods=['POST'])
@RequiredToken
def getDiagrams():
    data = request.get_json()
    print(data['uid'])
    x = getSQLDiagrams(data['uid'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "Diagrams Retrieved", "data": x})

@app.route('/getdiagram', methods=['POST'])
@RequiredToken
def getDiagram():
    data = request.get_json()
    x = getSQLDiagram(data['did'])

    if x == -1:
        return jsonify({"status": 500, "message": "Internal Server Error"})
    return jsonify({"status": 200, "message": "Diagram Retrieved", "data": x})

@app.route('/generate', methods=['POST'])
@RequiredToken
def generate():
    print("Generating")
    data = request.get_json()
    
    generateID = codeGenerate()
    while generateID in waitingData:
        generateID = codeGenerate()

    try:
        x = str(getResponse(data['description'], data['languages'],data['context']))
        print(x)
        y = ast.literal_eval(x)
        boxes_info = list(y['boxesInformation'].values())
        connections_info = y['connectionsInformation']

        waitingData.append([generateID, x])
        return jsonify({"status": 200, "message": "Response generated", "data": [boxes_info, connections_info], "id": generateID})
    except Exception as e:
        print(e)
        return jsonify({"status": 500, "message": "Internal Server Error"})

@app.route('/complete', methods=['POST'])
@RequiredToken
def complete():
    data = request.get_json()
    current = None

    for i in waitingData:
        if i[0] == data['id']:
            current = i[1]
            waitingData.remove(i)
            break

    if current == None:
        return jsonify({"status": 404, "message": "Not Found"})


    did = data['id']
    dim = data['dim']

    for i in range(len(dim)):
        dim[i] = ["B" + str(i+1), dim[i][0], dim[i][1]]

    data = ast.literal_eval(current)
    connections_info = data['connectionsInformation']

    print("CONNECTIONS_INFO",connections_info)
    print("BOXES_INFO",dim)

    placement = generatePlacement(dim, connections_info)

    return jsonify({"status": 200, "message": "Response completed", "data": placement, "id": did})

    
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404
