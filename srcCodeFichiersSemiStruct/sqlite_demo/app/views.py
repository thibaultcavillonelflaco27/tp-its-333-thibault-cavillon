from flask import Flask, render_template, request, redirect, url_for, make_response
import models
import jwt
import datetime

app = Flask(__name__)
models.init_db()

SECRET_KEY = "mysecretkey"
PASSWORD = "1234"  

@app.route('/')
def index():
    etudiants = models.get_etudiants()
    return render_template('index.html', etudiants=etudiants)

@app.route('/new')
def new_etudiant():
    return render_template('new.html')

@app.route('/auth', methods=['POST'])
def auth():
    nom = request.form['nom']
    addr = request.form['addr']
    pin = request.form['pin']
    password = request.form['password']
    if password != PASSWORD:
        return "Mot de passe incorrect", 403
    token = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")

    models.ajouter_etudiant(nom, addr, pin)

    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('token', token)
    return resp

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_etudiant(id):
    if request.method == 'POST':
        addr = request.form['addr']
        pin = request.form['pin']
        models.update_etudiant(id, addr, pin)
        return redirect(url_for('index'))

    etudiants = models.get_etudiants()
    etudiant = next((e for e in etudiants if e[0] == id), None)
    return render_template('new.html', etudiant=etudiant)

if __name__ == "__main__":
    app.run(debug=True)
