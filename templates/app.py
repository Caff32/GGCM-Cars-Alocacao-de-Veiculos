import os
from config import app
from flask import Flask, render_template, request, redirect,url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash


from flask_login import login_user, logout_user, login_required
from config import login_manager

from user import User


from pymongo import MongoClient
client = MongoClient('localhost',27017)
database = client['hertz']
collection = database.user



@login_manager.user_loader
def load_user(username):
    u = app.config['users'].find_one({"login": login})
    if not u:
        return None
    return User(u['_id'])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/operador',methods = ['GET', 'POST'])
def operador():
    if request.method == 'GET':
        return render_template('operadormain.html')





@app.route('/autenticacao', methods = ['GET', 'POST'])
def autenticacao():
    if request.method == 'GET':
            return render_template('autenticacao.html')





@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
        return render_template('autenticacao.html')

    collection.insert_one({
    'login': request.form['login2'],
    'email':  request.form['email2'],
    'password': generate_password_hash(request.form['senha2'])

    })

    return redirect(url_for('operador'))



def check_password(self, password):
    return check_password_hash(self['password'], password)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('autenticacao.html')

    retorno = collection.find_one({'login': request.form['login']})
    if retorno is None:
        return redirect(url_for('login'))


    if not check_password(retorno,request.form['senha']):
        return redirect(url_for('login'))

    usuario = retorno['login']
    login_user(retorno)

    return redirect(url_for('operador'))











if __name__ == '__main__':
    app.run(host = app.config['HOST'], port = app.config['PORT'], debug = app.config['DEBUG'])
