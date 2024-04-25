#Create a Standard Flask Server
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import json


app = Flask(__name__)
CORS(app)

from NeuroFlow.database import *
from NeuroFlow.validation import *

@app.route('/')
def home():
    return "<h1>NeuroFlow API</h1><p>This site is a prototype API for NeuroFlow.</p>"

@app.route('/checkdb')
def checkdb():
    if conn is not None:
        return jsonify({"status": 200, "message": "Connected to database"})
    else:
        return jsonify({"status": 500, "message": "Error connecting to database"})

@app.route('/login', methods=['POST'])
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
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404