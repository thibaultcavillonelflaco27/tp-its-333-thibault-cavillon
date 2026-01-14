from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

# Modèle Personne
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Créer la DB si elle n'existe pas
with app.app_context():
    db.create_all()

# CRUD minimal
@app.route("/persons", methods=["POST"])
def create_person():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name required"}), 400
    person = Person(name=data["name"])
    db.session.add(person)
    db.session.commit()
    return jsonify({"id": person.id, "name": person.name})

@app.route("/persons", methods=["GET"])
def get_persons():
    persons = Person.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in persons])

@app.route("/persons/<int:id>", methods=["DELETE"])
def delete_person(id):
    person = Person.query.get(id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Deleted"})

@app.route("/")
def index():
    return render_template("index.html")

# Important : écouter sur toutes les interfaces
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
