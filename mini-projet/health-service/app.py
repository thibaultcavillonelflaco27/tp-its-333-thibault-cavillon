from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import json
import os
import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change in production
CORS(app)
jwt = JWTManager(app)

DATA_FILE = "data.json"
PERSON_SERVICE_URL = "http://person-service:5001/persons"

# Créer fichier JSON vide si nécessaire
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def read_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Vérifier qu'une personne existe via le service Personne
def person_exists(person_id):
    try:
        resp = requests.get(f"{PERSON_SERVICE_URL}")
        if resp.status_code != 200:
            return False
        persons = resp.json()
        return any(p["id"] == int(person_id) for p in persons)
    except:
        return False

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == '1234':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/health/<int:person_id>", methods=["GET"])
def get_health(person_id):
    if not person_exists(person_id):
        return jsonify({"error": "Person not found"}), 404
    data = read_data()
    return jsonify(data.get(str(person_id), {}))

@app.route("/health/<int:person_id>", methods=["POST", "PUT"])
@jwt_required()
def add_or_update_health(person_id):
    if not person_exists(person_id):
        return jsonify({"error": "Person not found"}), 404
    data = request.get_json()
    all_data = read_data()
    all_data[str(person_id)] = data
    write_data(all_data)
    return jsonify(data)

@app.route("/health/<int:person_id>", methods=["DELETE"])
@jwt_required()
def delete_health(person_id):
    all_data = read_data()
    if str(person_id) in all_data:
        del all_data[str(person_id)]
        write_data(all_data)
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Data not found"}), 404

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
