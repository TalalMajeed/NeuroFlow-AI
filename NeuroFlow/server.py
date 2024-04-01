#Create a Standard Flask Server
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from NeuroFlow.database import *

@app.route('/')
def home():
    return "<h1>NeuroFlow API</h1><p>This site is a prototype API for NeuroFlow.</p>"

@app.route('/checkdb')
def checkdb():
    if conn is not None:
        return jsonify({"status": 200, "message": "Connected to database"})
    else:
        return jsonify({"status": 500, "message": "Error connecting to database"})

@app.route('/test')
def test():
    return jsonify({"status": 200, "message": "Success"})

@app.route('/users')
def users():
    return jsonify(getUsers())


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404