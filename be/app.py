from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from urllib.parse import quote_plus
import os

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
bcrypt = Bcrypt(app)

username = 'shivampkumar'
password = 'Need@4speed'
username = quote_plus(username)
password = quote_plus(password)

# MongoDB setup
uri = f"mongodb+srv://{username}:{password}@survivellm.jkaa8ma.mongodb.net/?retryWrites=true&w=majority&appName=survivellm"
client = MongoClient(uri)

db = client.patient_care_db
users = db.users

# def _corsify_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

@app.route('/api/hello', methods=['GET'])
@cross_origin()
def get_users():
    # Create a dummy result just to test if the API is working
    
    return jsonify({'message': 'API is working'}), 200

@app.route('/api/register', methods=['POST','OPTIONS'])
@cross_origin()
def register():
    user_data = request.json
    user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
    
    # Check if user already exists
    if users.find_one({'email': user_data['email']}):
        return jsonify({'message': 'User already exists'}), 400
    
    users.insert_one(user_data)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    user_data = request.json
    user = users.find_one({'email': user_data['email']})

    if user and bcrypt.check_password_hash(user['password'], user_data['password']):
        return jsonify({'message': 'Login successful', 'role': user['role']}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080)
