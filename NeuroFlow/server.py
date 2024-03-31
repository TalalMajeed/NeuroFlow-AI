#Create a Standard Flask Server
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "<h1>NeuroFlow API</h1><p>This site is a prototype API for NeuroFlow.</p>"