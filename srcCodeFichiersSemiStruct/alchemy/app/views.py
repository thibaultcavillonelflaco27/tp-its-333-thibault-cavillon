from flask import render_template, request, redirect, url_for, make_response, current_app
from app import app
from app import models
import jwt
import datetime
from functools import wraps

PASSWORD = "1234"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except Exception:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    etudiants = models.get_etudiants()
    return render_template('index.html', etudiants=etudiants)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != PASSWORD:
            return "Mot de passe incorrect", 403
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        resp = make_response(redirect(url_for('new_etudiant')))
        resp.set_cookie('token', token)
        return resp

    return render_template('login.html')


@app.route('/new')
@token_required
def new_etudiant():
    return render_template('new.html')


@app.route('/add', methods=['POST'])
@token_required
def add_etudiant():
    nom = request.form.get('nom')
    addr = request.form.get('addr')
    pin = request.form.get('pin')
    models.ajouter_etudiant(nom, addr, pin)
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@token_required
def edit_etudiant(id):
    if request.method == 'POST':
        addr = request.form.get('addr')
        pin = request.form.get('pin')
        models.update_etudiant(id, addr, pin)
        return redirect(url_for('index'))

    etudiants = models.get_etudiants()
    etudiant = next((e for e in etudiants if e.id == id), None)
    return render_template('new.html', etudiant=etudiant)


@app.route('/delete/<int:id>', methods=['POST'])
@token_required
def delete_etudiant(id):
    models.delete_etudiant(id)
    return redirect(url_for('index'))

