from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
from flask_cors import CORS
import jwt
import datetime
import json


app = Flask(__name__)
CORS(app)

from NeuroFlow.database import *
from NeuroFlow.validation import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def send_static(path):
    print("Requested path:", path)
    links = ["","login","panel","welcome","register"]
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
    
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404
